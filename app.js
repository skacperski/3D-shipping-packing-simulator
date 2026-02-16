import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { TransformControls } from 'three/addons/controls/TransformControls.js';

// ============================================
// Configuration
// ============================================

const ITEM_TYPES = {
    filly: {
        name: 'Filly Plush',
        dims: [33, 18, 10.5],
        color: 0xFF6B6B,
        emoji: '🧸'
    },
    dilly: {
        name: 'Dilly Plush',
        dims: [35, 18.5, 12],
        color: 0x4ECDC4,
        emoji: '🧸'
    },
    box: {
        name: 'Box',
        dims: [33, 9, 25],
        color: 0xFFD93D,
        emoji: '📦'
    },
    die: {
        name: 'Die',
        dims: [15, 15, 15],
        color: 0x6C5CE7,
        emoji: '🎲'
    }
};

const SCALE = 0.01; // cm to scene units
const COLLISION_COLOR = 0xff0000;
const SELECTED_EMISSIVE = 0x333366;

// ============================================
// State
// ============================================

let scene, camera, renderer, orbitControls, transformControls;
let containerMesh, containerBox;
let packedItems = [];
let selectedItem = null;
let snapEnabled = true;
let collisionEnabled = true;
let containerDims = { w: 60, h: 40, d: 40 };

// ============================================
// Initialize
// ============================================

function init() {
    const container = document.getElementById('canvas-container');

    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a24);

    // Camera
    const aspect = container.clientWidth / container.clientHeight;
    camera = new THREE.PerspectiveCamera(50, aspect, 0.01, 100);
    camera.position.set(0.8, 0.6, 0.8);

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const dirLight = new THREE.DirectionalLight(0xffffff, 1.2);
    dirLight.position.set(2, 3, 2);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.set(2048, 2048);
    dirLight.shadow.camera.near = 0.1;
    dirLight.shadow.camera.far = 20;
    dirLight.shadow.camera.left = -2;
    dirLight.shadow.camera.right = 2;
    dirLight.shadow.camera.top = 2;
    dirLight.shadow.camera.bottom = -2;
    scene.add(dirLight);

    const fillLight = new THREE.DirectionalLight(0x8888ff, 0.3);
    fillLight.position.set(-1, 1, -1);
    scene.add(fillLight);

    // Ground plane
    const groundGeometry = new THREE.PlaneGeometry(4, 4);
    const groundMaterial = new THREE.MeshStandardMaterial({
        color: 0x1e1e28,
        roughness: 0.9,
        metalness: 0.0
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.001;
    ground.receiveShadow = true;
    scene.add(ground);

    // Grid
    const gridHelper = new THREE.GridHelper(2, 40, 0x333344, 0x222233);
    gridHelper.position.y = 0.0001;
    scene.add(gridHelper);

    // Orbit Controls
    orbitControls = new OrbitControls(camera, renderer.domElement);
    orbitControls.enableDamping = true;
    orbitControls.dampingFactor = 0.08;
    orbitControls.target.set(0.3, 0.15, 0.15);
    orbitControls.minDistance = 0.2;
    orbitControls.maxDistance = 5;
    orbitControls.update();

    // Transform Controls (translate only - rotation via 90° buttons)
    transformControls = new TransformControls(camera, renderer.domElement);
    transformControls.setMode('translate');
    transformControls.addEventListener('dragging-changed', (event) => {
        orbitControls.enabled = !event.value;
    });
    transformControls.addEventListener('change', () => {
        if (selectedItem) {
            constrainToContainer(selectedItem);
            updateCollisions();
            updateStats();
        }
        render();
    });
    scene.add(transformControls.getHelper());

    applySnap();

    // Create container
    createContainer();

    // Raycaster for selection
    setupSelection();

    // UI events
    setupUI();

    // Keyboard shortcuts
    setupKeyboard();

    // Window resize
    window.addEventListener('resize', onResize);

    // Start render loop
    animate();
}

// ============================================
// Container
// ============================================

function createContainer() {
    if (containerMesh) {
        scene.remove(containerMesh);
    }

    const w = containerDims.w * SCALE;
    const h = containerDims.h * SCALE;
    const d = containerDims.d * SCALE;

    // Create wireframe container
    const group = new THREE.Group();

    // Bottom face (solid, slightly transparent)
    const bottomGeo = new THREE.PlaneGeometry(w, d);
    const bottomMat = new THREE.MeshStandardMaterial({
        color: 0x3a3a4a,
        roughness: 0.8,
        transparent: true,
        opacity: 0.3,
        side: THREE.DoubleSide
    });
    const bottom = new THREE.Mesh(bottomGeo, bottomMat);
    bottom.rotation.x = -Math.PI / 2;
    bottom.receiveShadow = true;
    group.add(bottom);

    // Edges of the container box
    const edgesGeo = new THREE.BoxGeometry(w, h, d);
    const edgesMat = new THREE.LineBasicMaterial({
        color: 0x6366f1,
        linewidth: 1,
        transparent: true,
        opacity: 0.7
    });
    const edges = new THREE.LineSegments(
        new THREE.EdgesGeometry(edgesGeo),
        edgesMat
    );
    edges.position.y = h / 2;
    group.add(edges);

    // Semi-transparent walls
    const wallMat = new THREE.MeshStandardMaterial({
        color: 0x4444aa,
        transparent: true,
        opacity: 0.06,
        side: THREE.DoubleSide,
        depthWrite: false
    });

    // Back wall
    const backWall = new THREE.Mesh(new THREE.PlaneGeometry(w, h), wallMat);
    backWall.position.set(0, h / 2, -d / 2);
    group.add(backWall);

    // Left wall
    const leftWall = new THREE.Mesh(new THREE.PlaneGeometry(d, h), wallMat);
    leftWall.rotation.y = Math.PI / 2;
    leftWall.position.set(-w / 2, h / 2, 0);
    group.add(leftWall);

    // Right wall
    const rightWall = new THREE.Mesh(new THREE.PlaneGeometry(d, h), wallMat);
    rightWall.rotation.y = -Math.PI / 2;
    rightWall.position.set(w / 2, h / 2, 0);
    group.add(rightWall);

    // Front wall (more transparent)
    const frontWallMat = new THREE.MeshStandardMaterial({
        color: 0x4444aa,
        transparent: true,
        opacity: 0.03,
        side: THREE.DoubleSide,
        depthWrite: false
    });
    const frontWall = new THREE.Mesh(new THREE.PlaneGeometry(w, h), frontWallMat);
    frontWall.position.set(0, h / 2, d / 2);
    group.add(frontWall);

    containerMesh = group;
    containerMesh.userData.isContainer = true;
    scene.add(containerMesh);

    // Update container bounding box
    containerBox = new THREE.Box3(
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(w, h, d)
    );

    // Center the container offset
    containerMesh.position.set(0, 0, 0);

    updateStats();
}

// ============================================
// Item Creation
// ============================================

function addItem(type) {
    const config = ITEM_TYPES[type];
    if (!config) return;

    const w = config.dims[0] * SCALE;
    const h = config.dims[1] * SCALE;
    const d = config.dims[2] * SCALE;

    const geometry = new THREE.BoxGeometry(w, h, d);
    const material = new THREE.MeshStandardMaterial({
        color: config.color,
        roughness: 0.5,
        metalness: 0.1,
        transparent: true,
        opacity: 0.85
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.castShadow = true;
    mesh.receiveShadow = true;

    // Add edge lines for visibility
    const edgeGeo = new THREE.EdgesGeometry(geometry);
    const edgeMat = new THREE.LineBasicMaterial({
        color: config.color,
        transparent: true,
        opacity: 0.5
    });
    const edgeLines = new THREE.LineSegments(edgeGeo, edgeMat);
    mesh.add(edgeLines);

    // Store item data
    mesh.userData = {
        type: type,
        config: config,
        originalDims: [...config.dims],
        id: Date.now() + Math.random(),
        isPackedItem: true
    };

    // Find a non-colliding position using simple placement
    const cwCm = containerDims.w;
    const chCm = containerDims.h;
    const cdCm = containerDims.d;

    const itemW = config.dims[0];
    const itemH = config.dims[1];
    const itemD = config.dims[2];

    // Gather existing AABBs
    const existingBoxes = packedItems.map(existing => {
        const bb = new THREE.Box3().setFromObject(existing);
        return {
            x: bb.min.x / SCALE,
            y: bb.min.y / SCALE,
            z: bb.min.z / SCALE,
            w: (bb.max.x - bb.min.x) / SCALE,
            h: (bb.max.y - bb.min.y) / SCALE,
            d: (bb.max.z - bb.min.z) / SCALE
        };
    });

    let placed = false;
    const candidates = [{ x: 0, y: 0, z: 0 }];
    for (const box of existingBoxes) {
        candidates.push({ x: box.x + box.w, y: box.y, z: box.z });
        candidates.push({ x: box.x, y: box.y + box.h, z: box.z });
        candidates.push({ x: box.x, y: box.y, z: box.z + box.d });
    }

    candidates.sort((a, b) => (a.y * 10000 + a.z * 100 + a.x) - (b.y * 10000 + b.z * 100 + b.x));

    for (const pos of candidates) {
        if (pos.x + itemW > cwCm + 0.01 || pos.y + itemH > chCm + 0.01 || pos.z + itemD > cdCm + 0.01) continue;
        if (pos.x < -0.01 || pos.y < -0.01 || pos.z < -0.01) continue;

        let collision = false;
        for (const box of existingBoxes) {
            if (pos.x < box.x + box.w - 0.01 && pos.x + itemW > box.x + 0.01 &&
                pos.y < box.y + box.h - 0.01 && pos.y + itemH > box.y + 0.01 &&
                pos.z < box.z + box.d - 0.01 && pos.z + itemD > box.z + 0.01) {
                collision = true;
                break;
            }
        }

        if (!collision) {
            mesh.position.set(
                (pos.x + itemW / 2) * SCALE,
                (pos.y + itemH / 2) * SCALE,
                (pos.z + itemD / 2) * SCALE
            );
            placed = true;
            break;
        }
    }

    if (!placed) {
        mesh.position.set(w / 2, h / 2, d / 2);
    }

    scene.add(mesh);
    packedItems.push(mesh);

    selectItem(mesh);
    updateItemsList();
    updateCollisions();
    updateStats();
    render();
}

// ============================================
// Selection
// ============================================

function setupSelection() {
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    renderer.domElement.addEventListener('pointerdown', (event) => {
        if (event.button !== 0) return;
        if (transformControls.dragging) return;

        const rect = renderer.domElement.getBoundingClientRect();
        mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
        mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

        raycaster.setFromCamera(mouse, camera);

        const meshes = packedItems.filter(item => item.parent === scene);
        const intersects = raycaster.intersectObjects(meshes, false);

        if (intersects.length > 0) {
            const hit = intersects[0].object;
            if (hit.userData.isPackedItem) {
                selectItem(hit);
            }
        } else {
            deselectItem();
        }
    });
}

function selectItem(mesh) {
    deselectItem();

    selectedItem = mesh;
    mesh.material.emissive.setHex(SELECTED_EMISSIVE);

    transformControls.attach(mesh);
    transformControls.setMode('translate');
    applySnap();

    document.getElementById('deleteSelected').disabled = false;

    const config = mesh.userData.config;
    document.getElementById('selectedInfo').textContent =
        `Selected: ${config.name} (${config.dims.join(' × ')} cm)`;

    updateItemsList();
    render();
}

function deselectItem() {
    if (selectedItem) {
        selectedItem.material.emissive.setHex(0x000000);
        selectedItem = null;
    }
    transformControls.detach();
    document.getElementById('deleteSelected').disabled = true;
    document.getElementById('selectedInfo').textContent = 'Click an item to select it';
    updateItemsList();
    render();
}

function deleteSelected() {
    if (!selectedItem) return;

    transformControls.detach();
    scene.remove(selectedItem);
    selectedItem.geometry.dispose();
    selectedItem.material.dispose();

    packedItems = packedItems.filter(item => item !== selectedItem);
    selectedItem = null;

    document.getElementById('deleteSelected').disabled = true;
    document.getElementById('selectedInfo').textContent = 'Click an item to select it';

    updateItemsList();
    updateCollisions();
    updateStats();
    render();
}

function clearAll() {
    transformControls.detach();
    selectedItem = null;

    packedItems.forEach(item => {
        scene.remove(item);
        item.geometry.dispose();
        item.material.dispose();
    });
    packedItems = [];

    document.getElementById('deleteSelected').disabled = true;
    document.getElementById('selectedInfo').textContent = 'Click an item to select it';

    updateItemsList();
    updateCollisions();
    updateStats();
    render();
}

// ============================================
// Constraints
// ============================================

function constrainToContainer(mesh) {
    if (!containerBox) return;

    const bbox = new THREE.Box3().setFromObject(mesh);
    const size = new THREE.Vector3();
    bbox.getSize(size);

    const cw = containerDims.w * SCALE;
    const ch = containerDims.h * SCALE;
    const cd = containerDims.d * SCALE;

    const halfW = size.x / 2;
    const halfH = size.y / 2;
    const halfD = size.z / 2;

    mesh.position.x = Math.max(halfW, Math.min(cw - halfW, mesh.position.x));
    mesh.position.y = Math.max(halfH, Math.min(ch - halfH, mesh.position.y));
    mesh.position.z = Math.max(halfD, Math.min(cd - halfD, mesh.position.z));
}

// ============================================
// Collision Detection (OBB-based)
// ============================================

function getOBB(mesh) {
    const config = mesh.userData.config;
    const w = config.dims[0] * SCALE;
    const h = config.dims[1] * SCALE;
    const d = config.dims[2] * SCALE;

    const halfExtents = new THREE.Vector3(w / 2, h / 2, d / 2);

    const rotationMatrix = new THREE.Matrix4().makeRotationFromQuaternion(mesh.quaternion);
    const axes = [
        new THREE.Vector3().setFromMatrixColumn(rotationMatrix, 0),
        new THREE.Vector3().setFromMatrixColumn(rotationMatrix, 1),
        new THREE.Vector3().setFromMatrixColumn(rotationMatrix, 2)
    ];

    return {
        center: mesh.position.clone(),
        halfExtents,
        axes
    };
}

function obbIntersects(a, b) {
    const EPSILON = 1e-6;

    const t = new THREE.Vector3().subVectors(b.center, a.center);
    const aAxes = a.axes;
    const bAxes = b.axes;
    const aHalf = a.halfExtents;
    const bHalf = b.halfExtents;

    const ae = [aHalf.x, aHalf.y, aHalf.z];
    const be = [bHalf.x, bHalf.y, bHalf.z];

    const R = [];
    const AbsR = [];

    for (let i = 0; i < 3; i++) {
        R[i] = [];
        AbsR[i] = [];
        for (let j = 0; j < 3; j++) {
            R[i][j] = aAxes[i].dot(bAxes[j]);
            AbsR[i][j] = Math.abs(R[i][j]) + EPSILON;
        }
    }

    const tLocal = [t.dot(aAxes[0]), t.dot(aAxes[1]), t.dot(aAxes[2])];

    // Test A's axes
    for (let i = 0; i < 3; i++) {
        const ra = ae[i];
        const rb = be[0] * AbsR[i][0] + be[1] * AbsR[i][1] + be[2] * AbsR[i][2];
        if (Math.abs(tLocal[i]) > ra + rb - EPSILON) return false;
    }

    // Test B's axes
    for (let j = 0; j < 3; j++) {
        const ra = ae[0] * AbsR[0][j] + ae[1] * AbsR[1][j] + ae[2] * AbsR[2][j];
        const rb = be[j];
        const tProj = tLocal[0] * R[0][j] + tLocal[1] * R[1][j] + tLocal[2] * R[2][j];
        if (Math.abs(tProj) > ra + rb - EPSILON) return false;
    }

    // Test cross products of axes
    // A0 x B0
    let ra = ae[1] * AbsR[2][0] + ae[2] * AbsR[1][0];
    let rb = be[1] * AbsR[0][2] + be[2] * AbsR[0][1];
    if (Math.abs(tLocal[2] * R[1][0] - tLocal[1] * R[2][0]) > ra + rb) return false;

    // A0 x B1
    ra = ae[1] * AbsR[2][1] + ae[2] * AbsR[1][1];
    rb = be[0] * AbsR[0][2] + be[2] * AbsR[0][0];
    if (Math.abs(tLocal[2] * R[1][1] - tLocal[1] * R[2][1]) > ra + rb) return false;

    // A0 x B2
    ra = ae[1] * AbsR[2][2] + ae[2] * AbsR[1][2];
    rb = be[0] * AbsR[0][1] + be[1] * AbsR[0][0];
    if (Math.abs(tLocal[2] * R[1][2] - tLocal[1] * R[2][2]) > ra + rb) return false;

    // A1 x B0
    ra = ae[0] * AbsR[2][0] + ae[2] * AbsR[0][0];
    rb = be[1] * AbsR[1][2] + be[2] * AbsR[1][1];
    if (Math.abs(tLocal[0] * R[2][0] - tLocal[2] * R[0][0]) > ra + rb) return false;

    // A1 x B1
    ra = ae[0] * AbsR[2][1] + ae[2] * AbsR[0][1];
    rb = be[0] * AbsR[1][2] + be[2] * AbsR[1][0];
    if (Math.abs(tLocal[0] * R[2][1] - tLocal[2] * R[0][1]) > ra + rb) return false;

    // A1 x B2
    ra = ae[0] * AbsR[2][2] + ae[2] * AbsR[0][2];
    rb = be[0] * AbsR[1][1] + be[1] * AbsR[1][0];
    if (Math.abs(tLocal[0] * R[2][2] - tLocal[2] * R[0][2]) > ra + rb) return false;

    // A2 x B0
    ra = ae[0] * AbsR[1][0] + ae[1] * AbsR[0][0];
    rb = be[1] * AbsR[2][2] + be[2] * AbsR[2][1];
    if (Math.abs(tLocal[1] * R[0][0] - tLocal[0] * R[1][0]) > ra + rb) return false;

    // A2 x B1
    ra = ae[0] * AbsR[1][1] + ae[1] * AbsR[0][1];
    rb = be[0] * AbsR[2][2] + be[2] * AbsR[2][0];
    if (Math.abs(tLocal[1] * R[0][1] - tLocal[0] * R[1][1]) > ra + rb) return false;

    // A2 x B2
    ra = ae[0] * AbsR[1][2] + ae[1] * AbsR[0][2];
    rb = be[0] * AbsR[2][1] + be[1] * AbsR[2][0];
    if (Math.abs(tLocal[1] * R[0][2] - tLocal[0] * R[1][2]) > ra + rb) return false;

    return true;
}

function isOutsideContainer(mesh) {
    const bbox = new THREE.Box3().setFromObject(mesh);
    const cw = containerDims.w * SCALE;
    const ch = containerDims.h * SCALE;
    const cd = containerDims.d * SCALE;
    const EPS = 0.005;
    return (
        bbox.min.x < -EPS || bbox.min.y < -EPS || bbox.min.z < -EPS ||
        bbox.max.x > cw + EPS || bbox.max.y > ch + EPS || bbox.max.z > cd + EPS
    );
}

function updateCollisions() {
    let collisionCount = 0;

    // Reset all colors
    packedItems.forEach(item => {
        const baseColor = item.userData.config.color;
        item.material.color.setHex(baseColor);
        if (item !== selectedItem) {
            item.material.emissive.setHex(0x000000);
        }
    });

    if (!collisionEnabled) {
        document.getElementById('statCollisions').textContent = '—';
        return;
    }

    const collisionSet = new Set();

    // Check inter-item collisions
    for (let i = 0; i < packedItems.length; i++) {
        for (let j = i + 1; j < packedItems.length; j++) {
            const obbA = getOBB(packedItems[i]);
            const obbB = getOBB(packedItems[j]);
            if (obbIntersects(obbA, obbB)) {
                collisionSet.add(packedItems[i]);
                collisionSet.add(packedItems[j]);
                collisionCount++;
            }
        }
    }

    // Check items outside container
    packedItems.forEach(item => {
        if (isOutsideContainer(item)) {
            collisionSet.add(item);
        }
    });

    collisionSet.forEach(item => {
        item.material.color.setHex(COLLISION_COLOR);
        if (item !== selectedItem) {
            item.material.emissive.setHex(0x330000);
        }
    });

    document.getElementById('statCollisions').textContent = collisionCount;
}

// ============================================
// Auto Pack (Greedy Bottom-Left-Back with AABB)
// ============================================

function autoPack() {
    if (packedItems.length === 0) return;

    const cw = containerDims.w;
    const ch = containerDims.h;
    const cd = containerDims.d;

    // Sort items by volume (largest first), then by longest dimension
    const sorted = [...packedItems].sort((a, b) => {
        const volA = a.userData.originalDims[0] * a.userData.originalDims[1] * a.userData.originalDims[2];
        const volB = b.userData.originalDims[0] * b.userData.originalDims[1] * b.userData.originalDims[2];
        return volB - volA;
    });

    // Reset all rotations first
    sorted.forEach(item => {
        item.quaternion.set(0, 0, 0, 1);
    });

    // Track placed item AABBs (in cm, axis-aligned)
    const placedBoxes = [];

    sorted.forEach(item => {
        const dims = item.userData.originalDims;

        // Generate all unique axis-aligned orientations
        const orientations = getUniqueOrientations(dims);

        let bestPos = null;
        let bestOrient = null;
        let bestScore = Infinity;

        for (const orient of orientations) {
            const [ow, oh, od] = orient.dims;

            // Check if this orientation fits in the container at all
            if (ow > cw || oh > ch || od > cd) continue;

            // Gather candidate positions: corners of existing boxes + origin
            const candidates = generateCandidatePositions(ow, oh, od, cw, ch, cd, placedBoxes);

            for (const pos of candidates) {
                // Verify the item fits within container bounds
                if (pos.x + ow > cw + 0.01 || pos.y + oh > ch + 0.01 || pos.z + od > cd + 0.01) continue;

                // Check for overlaps with all placed items
                let hasCollision = false;
                for (const box of placedBoxes) {
                    if (aabbOverlaps(pos.x, pos.y, pos.z, ow, oh, od, box.x, box.y, box.z, box.w, box.h, box.d)) {
                        hasCollision = true;
                        break;
                    }
                }

                if (!hasCollision) {
                    // Score: prefer bottom (y), then back (z), then left (x)
                    const score = pos.y * 10000 + pos.z * 100 + pos.x;
                    if (score < bestScore) {
                        bestScore = score;
                        bestPos = pos;
                        bestOrient = orient;
                    }
                }
            }
        }

        if (bestPos && bestOrient) {
            const [ow, oh, od] = bestOrient.dims;
            // Set position (center of the box in scene units)
            item.position.set(
                (bestPos.x + ow / 2) * SCALE,
                (bestPos.y + oh / 2) * SCALE,
                (bestPos.z + od / 2) * SCALE
            );
            item.quaternion.copy(bestOrient.quaternion);

            placedBoxes.push({
                x: bestPos.x,
                y: bestPos.y,
                z: bestPos.z,
                w: ow,
                h: oh,
                d: od
            });
        }
    });

    // Verify and constrain all items to container after packing
    sorted.forEach(item => constrainToContainer(item));

    updateCollisions();
    updateStats();
    updateItemsList();
    render();
}

function aabbOverlaps(ax, ay, az, aw, ah, ad, bx, by, bz, bw, bh, bd) {
    const EPS = 0.01;
    return (
        ax < bx + bw - EPS && ax + aw > bx + EPS &&
        ay < by + bh - EPS && ay + ah > by + EPS &&
        az < bz + bd - EPS && az + ad > bz + EPS
    );
}

function generateCandidatePositions(ow, oh, od, cw, ch, cd, placedBoxes) {
    const positions = [{ x: 0, y: 0, z: 0 }];

    for (const box of placedBoxes) {
        // Top of existing box
        positions.push({ x: box.x, y: box.y + box.h, z: box.z });
        // Right of existing box
        positions.push({ x: box.x + box.w, y: box.y, z: box.z });
        // Front of existing box
        positions.push({ x: box.x, y: box.y, z: box.z + box.d });
        // Aligned corners
        positions.push({ x: box.x + box.w, y: box.y, z: box.z + box.d });
        positions.push({ x: box.x + box.w, y: box.y + box.h, z: box.z });
        positions.push({ x: box.x, y: box.y + box.h, z: box.z + box.d });
    }

    // Remove out-of-bounds positions
    return positions.filter(p =>
        p.x >= -0.01 && p.y >= -0.01 && p.z >= -0.01 &&
        p.x + ow <= cw + 0.01 && p.y + oh <= ch + 0.01 && p.z + od <= cd + 0.01
    );
}

function getUniqueOrientations(dims) {
    const [a, b, c] = dims;

    const qx = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI / 2);
    const qy = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), Math.PI / 2);
    const qz = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 0, 1), Math.PI / 2);

    // Verified permutation-to-quaternion mapping:
    // BoxGeometry(a,b,c) has a on X, b on Y, c on Z
    // Rx90: Y->Z, Z->-Y => effective (a, c, b)
    // Ry90: X->-Z, Z->X => effective (c, b, a)
    // Rz90: X->Y, Y->-X => effective (b, a, c)
    // Rx90 then Ry90: => effective (b, c, a)
    // Ry90 then Rx90: => effective (c, a, b)
    const configs = [
        { dims: [a, b, c], q: new THREE.Quaternion() },
        { dims: [a, c, b], q: qx.clone() },
        { dims: [c, b, a], q: qy.clone() },
        { dims: [b, a, c], q: qz.clone() },
        { dims: [b, c, a], q: new THREE.Quaternion().multiplyQuaternions(qy, qx) },
        { dims: [c, a, b], q: new THREE.Quaternion().multiplyQuaternions(qx, qy) }
    ];

    // Remove duplicate dimension sets
    const seen = new Set();
    const orientations = [];
    for (const cfg of configs) {
        const key = cfg.dims.join(',');
        if (!seen.has(key)) {
            seen.add(key);
            orientations.push({ dims: cfg.dims, quaternion: cfg.q });
        }
    }

    return orientations;
}

// ============================================
// Snap
// ============================================

function applySnap() {
    if (snapEnabled) {
        transformControls.setTranslationSnap(0.005); // 0.5 cm
    } else {
        transformControls.setTranslationSnap(null);
    }
}

// ============================================
// Rotate 90° (discrete rotation)
// ============================================

function rotateItem90(axis, direction) {
    if (!selectedItem) return;

    const item = selectedItem;

    const angle = (Math.PI / 2) * direction;
    const axisVec = new THREE.Vector3(
        axis === 'x' ? 1 : 0,
        axis === 'y' ? 1 : 0,
        axis === 'z' ? 1 : 0
    );

    const rotQ = new THREE.Quaternion().setFromAxisAngle(axisVec, angle);
    item.quaternion.premultiply(rotQ);

    // Normalize quaternion to avoid drift
    item.quaternion.normalize();

    // Snap quaternion to nearest 90° aligned orientation
    snapQuaternionTo90(item.quaternion);

    // Update world matrix before constraining
    item.updateMatrixWorld(true);

    // Re-constrain to container after rotation
    constrainToContainer(item);

    updateCollisions();
    updateStats();

    // Re-assert selection (rotation may disrupt TransformControls state)
    selectItem(item);
}

function snapQuaternionTo90(q) {
    // Round each component to nearest value that represents a 90° rotation
    // Valid quaternion components for 90° multiples: 0, ±0.5, ±(√2/2), ±1
    const snap = (v) => {
        const vals = [0, 0.5, -0.5, Math.SQRT1_2, -Math.SQRT1_2, 1, -1];
        let closest = vals[0];
        let minDist = Math.abs(v - closest);
        for (const val of vals) {
            const dist = Math.abs(v - val);
            if (dist < minDist) {
                minDist = dist;
                closest = val;
            }
        }
        return closest;
    };

    q.x = snap(q.x);
    q.y = snap(q.y);
    q.z = snap(q.z);
    q.w = snap(q.w);
    q.normalize();
}

// ============================================
// UI
// ============================================

function setupUI() {
    // Add item buttons
    document.querySelectorAll('.btn-item').forEach(btn => {
        btn.addEventListener('click', () => {
            addItem(btn.dataset.type);
        });
    });

    // Rotate 90° buttons
    document.querySelectorAll('.btn-rotate').forEach(btn => {
        btn.addEventListener('click', () => {
            const axis = btn.dataset.axis;
            const dir = parseInt(btn.dataset.dir);
            rotateItem90(axis, dir);
        });
    });

    // Snap toggle
    document.getElementById('snapToggle').addEventListener('change', (e) => {
        snapEnabled = e.target.checked;
        applySnap();
    });

    document.getElementById('collisionToggle').addEventListener('change', (e) => {
        collisionEnabled = e.target.checked;
        updateCollisions();
        render();
    });

    // Action buttons
    document.getElementById('deleteSelected').addEventListener('click', deleteSelected);
    document.getElementById('clearAll').addEventListener('click', clearAll);
    document.getElementById('autoPackBtn').addEventListener('click', autoPack);

    // Container update
    document.getElementById('updateContainer').addEventListener('click', () => {
        containerDims.w = parseFloat(document.getElementById('containerW').value) || 60;
        containerDims.h = parseFloat(document.getElementById('containerH').value) || 40;
        containerDims.d = parseFloat(document.getElementById('containerD').value) || 40;
        createContainer();
        updateCollisions();
        render();
    });
}

function updateItemsList() {
    const list = document.getElementById('itemsList');
    const countEl = document.getElementById('itemCount');

    countEl.textContent = packedItems.length;

    if (packedItems.length === 0) {
        list.innerHTML = '<p class="empty-state">No items added yet</p>';
        return;
    }

    list.innerHTML = packedItems.map(item => {
        const config = item.userData.config;
        const isSelected = item === selectedItem;
        const colorHex = '#' + new THREE.Color(config.color).getHexString();
        return `
            <div class="item-entry ${isSelected ? 'selected' : ''}" data-id="${item.userData.id}">
                <span class="item-name">
                    <span class="color-dot" style="background:${colorHex}"></span>
                    ${config.emoji} ${config.name}
                </span>
                <button class="delete-item" data-id="${item.userData.id}" title="Delete">×</button>
            </div>
        `;
    }).join('');

    // Click to select
    list.querySelectorAll('.item-entry').forEach(entry => {
        entry.addEventListener('click', (e) => {
            if (e.target.classList.contains('delete-item')) return;
            const id = parseFloat(entry.dataset.id);
            const item = packedItems.find(i => i.userData.id === id);
            if (item) selectItem(item);
        });
    });

    // Delete buttons
    list.querySelectorAll('.delete-item').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = parseFloat(btn.dataset.id);
            const item = packedItems.find(i => i.userData.id === id);
            if (item) {
                if (item === selectedItem) {
                    deleteSelected();
                } else {
                    scene.remove(item);
                    item.geometry.dispose();
                    item.material.dispose();
                    packedItems = packedItems.filter(i => i !== item);
                    updateItemsList();
                    updateCollisions();
                    updateStats();
                    render();
                }
            }
        });
    });
}

function updateStats() {
    const cw = containerDims.w;
    const ch = containerDims.h;
    const cd = containerDims.d;
    const containerVol = cw * ch * cd;

    let itemsVol = 0;
    packedItems.forEach(item => {
        const dims = item.userData.config.dims;
        itemsVol += dims[0] * dims[1] * dims[2];
    });

    const pct = containerVol > 0 ? ((itemsVol / containerVol) * 100).toFixed(1) : 0;

    document.getElementById('statVolUsed').textContent = itemsVol.toLocaleString();
    document.getElementById('statVolTotal').textContent = containerVol.toLocaleString();
    document.getElementById('statPercent').textContent = pct + '%';
}

// ============================================
// Keyboard
// ============================================

function setupKeyboard() {
    window.addEventListener('keydown', (e) => {
        // Don't capture while typing in inputs
        if (e.target.tagName === 'INPUT') return;

        const dir = e.shiftKey ? -1 : 1;

        switch (e.key.toLowerCase()) {
            case 'x':
                e.preventDefault();
                rotateItem90('x', dir);
                break;
            case 'y':
                e.preventDefault();
                rotateItem90('y', dir);
                break;
            case 'z':
                e.preventDefault();
                rotateItem90('z', dir);
                break;
            case 'delete':
            case 'backspace':
                if (selectedItem) {
                    e.preventDefault();
                    deleteSelected();
                }
                break;
            case 'escape':
                deselectItem();
                break;
        }
    });
}

// ============================================
// Render Loop
// ============================================

function render() {
    renderer.render(scene, camera);
}

function animate() {
    requestAnimationFrame(animate);
    orbitControls.update();
    render();
}

function onResize() {
    const container = document.getElementById('canvas-container');
    const width = container.clientWidth;
    const height = container.clientHeight;

    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
    render();
}

// ============================================
// Start
// ============================================

init();
