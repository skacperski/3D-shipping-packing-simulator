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

const SCALE = 0.01;
const COLLISION_COLOR = 0xff0000;
const SELECTED_EMISSIVE = 0x333366;
const MAX_HISTORY = 50;

// ============================================
// State
// ============================================

let scene, camera, renderer, orbitControls, transformControls;
let packedItems = [];
let selectedItem = null;
let snapEnabled = true;
let collisionEnabled = true;

// Undo/Redo history
let undoStack = [];
let redoStack = [];
let isDragging = false;
let dragStartState = null;

// ============================================
// Initialize
// ============================================

function init() {
    const container = document.getElementById('canvas-container');

    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a24);

    const aspect = container.clientWidth / container.clientHeight;
    camera = new THREE.PerspectiveCamera(50, aspect, 0.01, 100);
    camera.position.set(0.8, 0.6, 0.8);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.appendChild(renderer.domElement);

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

    const groundGeometry = new THREE.PlaneGeometry(4, 4);
    const groundMaterial = new THREE.MeshStandardMaterial({
        color: 0x1e1e28, roughness: 0.9, metalness: 0.0
    });
    const ground = new THREE.Mesh(groundGeometry, groundMaterial);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.001;
    ground.receiveShadow = true;
    scene.add(ground);

    const gridHelper = new THREE.GridHelper(2, 40, 0x333344, 0x222233);
    gridHelper.position.y = 0.0001;
    scene.add(gridHelper);

    orbitControls = new OrbitControls(camera, renderer.domElement);
    orbitControls.enableDamping = true;
    orbitControls.dampingFactor = 0.08;
    orbitControls.target.set(0.3, 0.15, 0.15);
    orbitControls.minDistance = 0.2;
    orbitControls.maxDistance = 5;
    orbitControls.update();

    transformControls = new TransformControls(camera, renderer.domElement);
    transformControls.setMode('translate');
    transformControls.addEventListener('dragging-changed', (event) => {
        orbitControls.enabled = !event.value;
        if (event.value) {
            // Drag started - save state
            isDragging = true;
            dragStartState = captureState();
        } else {
            // Drag ended - push undo
            if (isDragging && dragStartState) {
                pushUndo(dragStartState);
                dragStartState = null;
            }
            isDragging = false;
        }
    });
    transformControls.addEventListener('change', () => {
        if (selectedItem) {
            updateCollisions();
            updateStats();
        }
        render();
    });
    scene.add(transformControls.getHelper());

    applySnap();
    setupSelection();
    setupUI();
    setupKeyboard();

    window.addEventListener('resize', onResize);
    animate();
}

// ============================================
// Undo / Redo System
// ============================================

function captureState() {
    return packedItems.map(item => ({
        id: item.userData.id,
        type: item.userData.type,
        px: item.position.x,
        py: item.position.y,
        pz: item.position.z,
        qx: item.quaternion.x,
        qy: item.quaternion.y,
        qz: item.quaternion.z,
        qw: item.quaternion.w
    }));
}

function pushUndo(stateBefore) {
    if (!stateBefore) stateBefore = captureState();
    undoStack.push(stateBefore);
    if (undoStack.length > MAX_HISTORY) undoStack.shift();
    redoStack = [];
    updateUndoRedoButtons();
}

function restoreState(state) {
    deselectItem();

    // Build lookup of existing items by id
    const existingMap = new Map();
    packedItems.forEach(item => existingMap.set(item.userData.id, item));

    const stateIds = new Set(state.map(s => s.id));

    // Remove items not in the state
    packedItems.forEach(item => {
        if (!stateIds.has(item.userData.id)) {
            scene.remove(item);
            item.geometry.dispose();
            item.material.dispose();
        }
    });

    // Add or update items from state
    const newPackedItems = [];
    state.forEach(s => {
        let item = existingMap.get(s.id);
        if (!item) {
            // Item was deleted - recreate it
            item = createItemMesh(s.type, s.id);
            scene.add(item);
        }
        item.position.set(s.px, s.py, s.pz);
        item.quaternion.set(s.qx, s.qy, s.qz, s.qw);
        newPackedItems.push(item);
    });

    packedItems = newPackedItems;
    updateCollisions();
    updateStats();
    updateItemsList();
    render();
}

function undo() {
    if (undoStack.length === 0) return;
    const currentState = captureState();
    redoStack.push(currentState);
    const prevState = undoStack.pop();
    restoreState(prevState);
    updateUndoRedoButtons();
}

function redo() {
    if (redoStack.length === 0) return;
    const currentState = captureState();
    undoStack.push(currentState);
    const nextState = redoStack.pop();
    restoreState(nextState);
    updateUndoRedoButtons();
}

function updateUndoRedoButtons() {
    const undoBtn = document.getElementById('undoBtn');
    const redoBtn = document.getElementById('redoBtn');
    if (undoBtn) undoBtn.disabled = undoStack.length === 0;
    if (redoBtn) redoBtn.disabled = redoStack.length === 0;
}

// Helper to create a mesh without placing it (for undo restore)
function createItemMesh(type, id) {
    const config = ITEM_TYPES[type];
    const w = config.dims[0] * SCALE;
    const h = config.dims[1] * SCALE;
    const d = config.dims[2] * SCALE;

    const geometry = new THREE.BoxGeometry(w, h, d);
    const material = new THREE.MeshStandardMaterial({
        color: config.color, roughness: 0.5, metalness: 0.1,
        transparent: true, opacity: 0.85
    });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.castShadow = true;
    mesh.receiveShadow = true;

    const edgeGeo = new THREE.EdgesGeometry(geometry);
    const edgeMat = new THREE.LineBasicMaterial({
        color: config.color, transparent: true, opacity: 0.5
    });
    mesh.add(new THREE.LineSegments(edgeGeo, edgeMat));

    mesh.userData = {
        type, config, originalDims: [...config.dims],
        id: id || (Date.now() + Math.random()),
        isPackedItem: true
    };
    return mesh;
}

// ============================================
// Item Creation
// ============================================

function addItem(type) {
    const before = captureState();
    const config = ITEM_TYPES[type];
    if (!config) return;

    const mesh = createItemMesh(type);

    const itemW = config.dims[0];
    const itemH = config.dims[1];
    const itemD = config.dims[2];

    // Place next to existing items using candidate positions
    const existingBoxes = packedItems.map(existing => {
        const bb = new THREE.Box3().setFromObject(existing);
        return {
            x: bb.min.x / SCALE, y: bb.min.y / SCALE, z: bb.min.z / SCALE,
            w: (bb.max.x - bb.min.x) / SCALE, h: (bb.max.y - bb.min.y) / SCALE,
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
        mesh.position.set(
            (itemW / 2) * SCALE,
            (itemH / 2) * SCALE,
            (itemD / 2) * SCALE
        );
    }

    scene.add(mesh);
    packedItems.push(mesh);
    pushUndo(before);

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
            if (hit.userData.isPackedItem) selectItem(hit);
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
    const before = captureState();

    transformControls.detach();
    scene.remove(selectedItem);
    selectedItem.geometry.dispose();
    selectedItem.material.dispose();
    packedItems = packedItems.filter(item => item !== selectedItem);
    selectedItem = null;

    pushUndo(before);
    document.getElementById('deleteSelected').disabled = true;
    document.getElementById('selectedInfo').textContent = 'Click an item to select it';
    updateItemsList();
    updateCollisions();
    updateStats();
    render();
}

function clearAll() {
    if (packedItems.length === 0) return;
    const before = captureState();

    transformControls.detach();
    selectedItem = null;
    packedItems.forEach(item => {
        scene.remove(item);
        item.geometry.dispose();
        item.material.dispose();
    });
    packedItems = [];

    pushUndo(before);
    document.getElementById('deleteSelected').disabled = true;
    document.getElementById('selectedInfo').textContent = 'Click an item to select it';
    updateItemsList();
    updateCollisions();
    updateStats();
    render();
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
    return { center: mesh.position.clone(), halfExtents, axes };
}

function obbIntersects(a, b) {
    const EPSILON = 1e-6;
    const t = new THREE.Vector3().subVectors(b.center, a.center);
    const ae = [a.halfExtents.x, a.halfExtents.y, a.halfExtents.z];
    const be = [b.halfExtents.x, b.halfExtents.y, b.halfExtents.z];
    const R = [], AbsR = [];

    for (let i = 0; i < 3; i++) {
        R[i] = []; AbsR[i] = [];
        for (let j = 0; j < 3; j++) {
            R[i][j] = a.axes[i].dot(b.axes[j]);
            AbsR[i][j] = Math.abs(R[i][j]) + EPSILON;
        }
    }
    const tL = [t.dot(a.axes[0]), t.dot(a.axes[1]), t.dot(a.axes[2])];

    for (let i = 0; i < 3; i++) {
        if (Math.abs(tL[i]) > ae[i] + be[0] * AbsR[i][0] + be[1] * AbsR[i][1] + be[2] * AbsR[i][2] - EPSILON) return false;
    }
    for (let j = 0; j < 3; j++) {
        if (Math.abs(tL[0] * R[0][j] + tL[1] * R[1][j] + tL[2] * R[2][j]) > ae[0] * AbsR[0][j] + ae[1] * AbsR[1][j] + ae[2] * AbsR[2][j] + be[j] - EPSILON) return false;
    }

    let ra, rb;
    ra = ae[1]*AbsR[2][0]+ae[2]*AbsR[1][0]; rb = be[1]*AbsR[0][2]+be[2]*AbsR[0][1];
    if (Math.abs(tL[2]*R[1][0]-tL[1]*R[2][0]) > ra+rb) return false;
    ra = ae[1]*AbsR[2][1]+ae[2]*AbsR[1][1]; rb = be[0]*AbsR[0][2]+be[2]*AbsR[0][0];
    if (Math.abs(tL[2]*R[1][1]-tL[1]*R[2][1]) > ra+rb) return false;
    ra = ae[1]*AbsR[2][2]+ae[2]*AbsR[1][2]; rb = be[0]*AbsR[0][1]+be[1]*AbsR[0][0];
    if (Math.abs(tL[2]*R[1][2]-tL[1]*R[2][2]) > ra+rb) return false;
    ra = ae[0]*AbsR[2][0]+ae[2]*AbsR[0][0]; rb = be[1]*AbsR[1][2]+be[2]*AbsR[1][1];
    if (Math.abs(tL[0]*R[2][0]-tL[2]*R[0][0]) > ra+rb) return false;
    ra = ae[0]*AbsR[2][1]+ae[2]*AbsR[0][1]; rb = be[0]*AbsR[1][2]+be[2]*AbsR[1][0];
    if (Math.abs(tL[0]*R[2][1]-tL[2]*R[0][1]) > ra+rb) return false;
    ra = ae[0]*AbsR[2][2]+ae[2]*AbsR[0][2]; rb = be[0]*AbsR[1][1]+be[1]*AbsR[1][0];
    if (Math.abs(tL[0]*R[2][2]-tL[2]*R[0][2]) > ra+rb) return false;
    ra = ae[0]*AbsR[1][0]+ae[1]*AbsR[0][0]; rb = be[1]*AbsR[2][2]+be[2]*AbsR[2][1];
    if (Math.abs(tL[1]*R[0][0]-tL[0]*R[1][0]) > ra+rb) return false;
    ra = ae[0]*AbsR[1][1]+ae[1]*AbsR[0][1]; rb = be[0]*AbsR[2][2]+be[2]*AbsR[2][0];
    if (Math.abs(tL[1]*R[0][1]-tL[0]*R[1][1]) > ra+rb) return false;
    ra = ae[0]*AbsR[1][2]+ae[1]*AbsR[0][2]; rb = be[0]*AbsR[2][1]+be[1]*AbsR[2][0];
    if (Math.abs(tL[1]*R[0][2]-tL[0]*R[1][2]) > ra+rb) return false;

    return true;
}

function updateCollisions() {
    let collisionCount = 0;
    packedItems.forEach(item => {
        item.material.color.setHex(item.userData.config.color);
        if (item !== selectedItem) item.material.emissive.setHex(0x000000);
    });

    if (!collisionEnabled) {
        document.getElementById('statCollisions').textContent = '—';
        return;
    }

    const collisionSet = new Set();
    for (let i = 0; i < packedItems.length; i++) {
        for (let j = i + 1; j < packedItems.length; j++) {
            if (obbIntersects(getOBB(packedItems[i]), getOBB(packedItems[j]))) {
                collisionSet.add(packedItems[i]);
                collisionSet.add(packedItems[j]);
                collisionCount++;
            }
        }
    }
    collisionSet.forEach(item => {
        item.material.color.setHex(COLLISION_COLOR);
        if (item !== selectedItem) item.material.emissive.setHex(0x330000);
    });
    document.getElementById('statCollisions').textContent = collisionCount;
}

// ============================================
// Packing Algorithms - Shared Helpers
// ============================================

function aabbOverlaps(ax, ay, az, aw, ah, ad, bx, by, bz, bw, bh, bd) {
    const EPS = 0.01;
    return (ax < bx+bw-EPS && ax+aw > bx+EPS && ay < by+bh-EPS && ay+ah > by+EPS && az < bz+bd-EPS && az+ad > bz+EPS);
}

function generateCandidatePositions(ow, oh, od, placedBoxes) {
    const positions = [{ x: 0, y: 0, z: 0 }];
    for (const box of placedBoxes) {
        positions.push({ x: box.x, y: box.y + box.h, z: box.z });
        positions.push({ x: box.x + box.w, y: box.y, z: box.z });
        positions.push({ x: box.x, y: box.y, z: box.z + box.d });
        positions.push({ x: box.x + box.w, y: box.y, z: box.z + box.d });
        positions.push({ x: box.x + box.w, y: box.y + box.h, z: box.z });
        positions.push({ x: box.x, y: box.y + box.h, z: box.z + box.d });
    }
    return positions.filter(p => p.x >= -0.01 && p.y >= -0.01 && p.z >= -0.01);
}

function getUniqueOrientations(dims) {
    const [a, b, c] = dims;
    const qx = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(1, 0, 0), Math.PI / 2);
    const qy = new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 1, 0), Math.PI / 2);
    const configs = [
        { dims: [a, b, c], q: new THREE.Quaternion() },
        { dims: [a, c, b], q: qx.clone() },
        { dims: [c, b, a], q: qy.clone() },
        { dims: [b, a, c], q: new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0, 0, 1), Math.PI / 2) },
        { dims: [b, c, a], q: new THREE.Quaternion().multiplyQuaternions(qy, qx) },
        { dims: [c, a, b], q: new THREE.Quaternion().multiplyQuaternions(qx, qy) }
    ];
    const seen = new Set();
    const orientations = [];
    for (const cfg of configs) {
        const key = cfg.dims.join(',');
        if (!seen.has(key)) { seen.add(key); orientations.push({ dims: cfg.dims, quaternion: cfg.q }); }
    }
    return orientations;
}

// Run a single packing attempt with a given item order and scoring function
function runPackingAttempt(itemsList, scoreFn) {
    const placedBoxes = [];
    const results = [];

    for (const item of itemsList) {
        const dims = item.userData.originalDims;
        const orientations = getUniqueOrientations(dims);

        let bestPos = null, bestOrient = null, bestScore = Infinity;

        for (const orient of orientations) {
            const [ow, oh, od] = orient.dims;

            const candidates = generateCandidatePositions(ow, oh, od, placedBoxes);
            for (const pos of candidates) {
                let hasCollision = false;
                for (const box of placedBoxes) {
                    if (aabbOverlaps(pos.x, pos.y, pos.z, ow, oh, od, box.x, box.y, box.z, box.w, box.h, box.d)) {
                        hasCollision = true; break;
                    }
                }
                if (!hasCollision) {
                    const score = scoreFn(pos, ow, oh, od, placedBoxes);
                    if (score < bestScore) { bestScore = score; bestPos = pos; bestOrient = orient; }
                }
            }
        }

        if (bestPos && bestOrient) {
            const [ow, oh, od] = bestOrient.dims;
            placedBoxes.push({ x: bestPos.x, y: bestPos.y, z: bestPos.z, w: ow, h: oh, d: od });
            results.push({ item, pos: bestPos, orient: bestOrient });
        } else {
            results.push({ item, pos: null, orient: null });
        }
    }
    return { placedBoxes, results };
}

// Calculate bounding box height for packed result
function getPackedHeight(placedBoxes) {
    let maxY = 0;
    for (const box of placedBoxes) maxY = Math.max(maxY, box.y + box.h);
    return maxY;
}

function getPackedBoundingVolume(placedBoxes) {
    let maxX = 0, maxY = 0, maxZ = 0;
    for (const box of placedBoxes) {
        maxX = Math.max(maxX, box.x + box.w);
        maxY = Math.max(maxY, box.y + box.h);
        maxZ = Math.max(maxZ, box.z + box.d);
    }
    return maxX * maxY * maxZ;
}

function applyPackingResult(results) {
    results.forEach(r => {
        if (r.pos && r.orient) {
            const [ow, oh, od] = r.orient.dims;
            r.item.position.set(
                (r.pos.x + ow / 2) * SCALE,
                (r.pos.y + oh / 2) * SCALE,
                (r.pos.z + od / 2) * SCALE
            );
            r.item.quaternion.copy(r.orient.quaternion);
        }
    });
}

// ============================================
// Auto Pack (same as before)
// ============================================

function autoPack() {
    if (packedItems.length === 0) return;
    const before = captureState();

    const sorted = [...packedItems].sort((a, b) => {
        const volA = a.userData.originalDims.reduce((p, c) => p * c, 1);
        const volB = b.userData.originalDims.reduce((p, c) => p * c, 1);
        return volB - volA;
    });
    sorted.forEach(item => item.quaternion.set(0, 0, 0, 1));

    const scoreFn = (pos, ow, oh, od) => pos.y * 10000 + pos.z * 100 + pos.x;
    const result = runPackingAttempt(sorted, scoreFn);
    applyPackingResult(result.results);

    pushUndo(before);
    updateCollisions();
    updateStats();
    updateItemsList();
    render();
}

// ============================================
// Random Placement
// ============================================

function randomPlace() {
    if (packedItems.length === 0) return;
    const before = captureState();

    // Compute a reasonable random area based on total item volume
    let totalVol = 0;
    packedItems.forEach(item => {
        const d = item.userData.originalDims;
        totalVol += d[0] * d[1] * d[2];
    });
    const spread = Math.cbrt(totalVol) * 2.5;

    const shuffled = [...packedItems].sort(() => Math.random() - 0.5);
    shuffled.forEach(item => item.quaternion.set(0, 0, 0, 1));

    const placedBoxes = [];

    shuffled.forEach(item => {
        const dims = item.userData.originalDims;
        const orientations = getUniqueOrientations(dims);
        const orient = orientations[Math.floor(Math.random() * orientations.length)];
        const [ow, oh, od] = orient.dims;

        let placed = false;
        for (let attempt = 0; attempt < 200; attempt++) {
            const px = Math.random() * spread;
            const py = Math.random() * spread;
            const pz = Math.random() * spread;

            let collision = false;
            for (const box of placedBoxes) {
                if (aabbOverlaps(px, py, pz, ow, oh, od, box.x, box.y, box.z, box.w, box.h, box.d)) {
                    collision = true; break;
                }
            }
            if (!collision) {
                item.position.set((px + ow / 2) * SCALE, (py + oh / 2) * SCALE, (pz + od / 2) * SCALE);
                item.quaternion.copy(orient.quaternion);
                placedBoxes.push({ x: px, y: py, z: pz, w: ow, h: oh, d: od });
                placed = true;
                break;
            }
        }

        if (!placed) {
            const candidates = generateCandidatePositions(ow, oh, od, placedBoxes);
            for (const pos of candidates) {
                let collision = false;
                for (const box of placedBoxes) {
                    if (aabbOverlaps(pos.x, pos.y, pos.z, ow, oh, od, box.x, box.y, box.z, box.w, box.h, box.d)) {
                        collision = true; break;
                    }
                }
                if (!collision) {
                    item.position.set((pos.x + ow / 2) * SCALE, (pos.y + oh / 2) * SCALE, (pos.z + od / 2) * SCALE);
                    item.quaternion.copy(orient.quaternion);
                    placedBoxes.push({ x: pos.x, y: pos.y, z: pos.z, w: ow, h: oh, d: od });
                    break;
                }
            }
        }
    });

    pushUndo(before);
    updateCollisions();
    updateStats();
    updateItemsList();
    render();
}

// ============================================
// Optimal Packing (tries many strategies)
// ============================================

function optimalPack() {
    if (packedItems.length === 0) return;
    const before = captureState();

    const scoreFunctions = [
        (pos, ow, oh, od) => pos.y * 10000 + pos.z * 100 + pos.x,
        (pos, ow, oh, od) => pos.y * 10000 + pos.x * 100 + pos.z,
        (pos, ow, oh, od) => pos.y * 10000 + (pos.x + pos.z) * 50,
        (pos, ow, oh, od) => (pos.y + oh) * 10000 + pos.x * 100 + pos.z,
        // Prefer touching origin walls
        (pos, ow, oh, od, placed) => {
            let contact = 0;
            if (pos.x < 0.1) contact++;
            if (pos.y < 0.1) contact++;
            if (pos.z < 0.1) contact++;
            for (const b of placed) {
                if (Math.abs(pos.x - (b.x + b.w)) < 0.1 || Math.abs(pos.x + ow - b.x) < 0.1) contact++;
                if (Math.abs(pos.y - (b.y + b.h)) < 0.1) contact++;
                if (Math.abs(pos.z - (b.z + b.d)) < 0.1 || Math.abs(pos.z + od - b.z) < 0.1) contact++;
            }
            return -contact * 10000 + pos.y * 1000 + pos.x + pos.z;
        },
        (pos, ow, oh, od) => pos.y * 5000 + pos.x * 50 + pos.z,
    ];

    const sortingStrategies = [
        (a, b) => b.userData.originalDims.reduce((p, c) => p * c, 1) - a.userData.originalDims.reduce((p, c) => p * c, 1),
        (a, b) => Math.max(...b.userData.originalDims) - Math.max(...a.userData.originalDims),
        (a, b) => {
            const aD = [...a.userData.originalDims].sort((x, y) => y - x);
            const bD = [...b.userData.originalDims].sort((x, y) => y - x);
            return (bD[0] * bD[1]) - (aD[0] * aD[1]);
        },
        (a, b) => Math.min(...a.userData.originalDims) - Math.min(...b.userData.originalDims),
    ];

    let bestResult = null;
    let bestBoundingVol = Infinity;

    for (const sortFn of sortingStrategies) {
        for (const scoreFn of scoreFunctions) {
            const sorted = [...packedItems].sort(sortFn);
            sorted.forEach(item => item.quaternion.set(0, 0, 0, 1));

            const result = runPackingAttempt(sorted, scoreFn);
            const allPlaced = result.results.every(r => r.pos !== null);
            if (!allPlaced) continue;

            const vol = getPackedBoundingVolume(result.placedBoxes);
            if (vol < bestBoundingVol) { bestBoundingVol = vol; bestResult = result; }
        }
    }

    for (let attempt = 0; attempt < 30; attempt++) {
        const shuffled = [...packedItems].sort(() => Math.random() - 0.5);
        shuffled.forEach(item => item.quaternion.set(0, 0, 0, 1));

        const scoreFn = scoreFunctions[attempt % scoreFunctions.length];
        const result = runPackingAttempt(shuffled, scoreFn);
        const allPlaced = result.results.every(r => r.pos !== null);
        if (!allPlaced) continue;

        const vol = getPackedBoundingVolume(result.placedBoxes);
        if (vol < bestBoundingVol) { bestBoundingVol = vol; bestResult = result; }
    }

    if (bestResult) {
        applyPackingResult(bestResult.results);
    }

    pushUndo(before);
    updateCollisions();
    updateStats();
    updateItemsList();
    render();

    if (bestResult) {
        const h = getPackedHeight(bestResult.placedBoxes);
        document.getElementById('selectedInfo').textContent =
            `Optimal: height ${h.toFixed(1)} cm, bounding vol ${bestBoundingVol.toFixed(0)} cm³`;
    }
}

// ============================================
// Snap
// ============================================

function applySnap() {
    if (snapEnabled) {
        transformControls.setTranslationSnap(0.005);
    } else {
        transformControls.setTranslationSnap(null);
    }
}

// ============================================
// Rotate 90°
// ============================================

function rotateItem90(axis, direction) {
    if (!selectedItem) return;
    const before = captureState();
    const item = selectedItem;

    const angle = (Math.PI / 2) * direction;
    const axisVec = new THREE.Vector3(
        axis === 'x' ? 1 : 0, axis === 'y' ? 1 : 0, axis === 'z' ? 1 : 0
    );

    item.quaternion.premultiply(new THREE.Quaternion().setFromAxisAngle(axisVec, angle));
    item.quaternion.normalize();
    snapQuaternionTo90(item.quaternion);
    item.updateMatrixWorld(true);

    pushUndo(before);
    updateCollisions();
    updateStats();
    selectItem(item);
}

function snapQuaternionTo90(q) {
    const snap = (v) => {
        const vals = [0, 0.5, -0.5, Math.SQRT1_2, -Math.SQRT1_2, 1, -1];
        let closest = vals[0], minDist = Math.abs(v);
        for (const val of vals) {
            const dist = Math.abs(v - val);
            if (dist < minDist) { minDist = dist; closest = val; }
        }
        return closest;
    };
    q.x = snap(q.x); q.y = snap(q.y); q.z = snap(q.z); q.w = snap(q.w);
    q.normalize();
}

// ============================================
// UI
// ============================================

function setupUI() {
    document.querySelectorAll('.btn-item').forEach(btn => {
        btn.addEventListener('click', () => addItem(btn.dataset.type));
    });

    document.querySelectorAll('.btn-rotate').forEach(btn => {
        btn.addEventListener('click', () => {
            rotateItem90(btn.dataset.axis, parseInt(btn.dataset.dir));
        });
    });

    document.getElementById('snapToggle').addEventListener('change', (e) => {
        snapEnabled = e.target.checked; applySnap();
    });
    document.getElementById('collisionToggle').addEventListener('change', (e) => {
        collisionEnabled = e.target.checked; updateCollisions(); render();
    });

    document.getElementById('deleteSelected').addEventListener('click', deleteSelected);
    document.getElementById('clearAll').addEventListener('click', clearAll);
    document.getElementById('autoPackBtn').addEventListener('click', autoPack);
    document.getElementById('randomPackBtn').addEventListener('click', randomPlace);
    document.getElementById('optimalPackBtn').addEventListener('click', optimalPack);
    document.getElementById('undoBtn').addEventListener('click', undo);
    document.getElementById('redoBtn').addEventListener('click', redo);

    updateUndoRedoButtons();
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
        return `<div class="item-entry ${isSelected ? 'selected' : ''}" data-id="${item.userData.id}">
            <span class="item-name"><span class="color-dot" style="background:${colorHex}"></span>${config.emoji} ${config.name}</span>
            <button class="delete-item" data-id="${item.userData.id}" title="Delete">×</button>
        </div>`;
    }).join('');

    list.querySelectorAll('.item-entry').forEach(entry => {
        entry.addEventListener('click', (e) => {
            if (e.target.classList.contains('delete-item')) return;
            const id = parseFloat(entry.dataset.id);
            const item = packedItems.find(i => i.userData.id === id);
            if (item) selectItem(item);
        });
    });

    list.querySelectorAll('.delete-item').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = parseFloat(btn.dataset.id);
            const item = packedItems.find(i => i.userData.id === id);
            if (item) {
                if (item === selectedItem) { deleteSelected(); }
                else {
                    const before = captureState();
                    scene.remove(item);
                    item.geometry.dispose();
                    item.material.dispose();
                    packedItems = packedItems.filter(i => i !== item);
                    pushUndo(before);
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
    let itemsVol = 0;
    packedItems.forEach(item => {
        const dims = item.userData.config.dims;
        itemsVol += dims[0] * dims[1] * dims[2];
    });
    document.getElementById('statVolUsed').textContent = itemsVol.toLocaleString();

    if (packedItems.length === 0) {
        document.getElementById('statBBox').textContent = '—';
        document.getElementById('statBBoxVol').textContent = '0';
        return;
    }

    // Compute bounding box of all items
    const totalBBox = new THREE.Box3();
    packedItems.forEach(item => {
        totalBBox.expandByObject(item);
    });
    const size = new THREE.Vector3();
    totalBBox.getSize(size);
    const bw = (size.x / SCALE).toFixed(1);
    const bh = (size.y / SCALE).toFixed(1);
    const bd = (size.z / SCALE).toFixed(1);
    const bboxVol = (size.x / SCALE) * (size.y / SCALE) * (size.z / SCALE);

    document.getElementById('statBBox').textContent = `${bw}×${bh}×${bd}`;
    document.getElementById('statBBoxVol').textContent = Math.round(bboxVol).toLocaleString();
}

// ============================================
// Keyboard
// ============================================

function setupKeyboard() {
    window.addEventListener('keydown', (e) => {
        if (e.target.tagName === 'INPUT') return;

        // Undo/Redo
        if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'z') {
            e.preventDefault();
            if (e.shiftKey) { redo(); } else { undo(); }
            return;
        }
        if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'y') {
            e.preventDefault();
            redo();
            return;
        }

        const dir = e.shiftKey ? -1 : 1;
        switch (e.key.toLowerCase()) {
            case 'x': e.preventDefault(); rotateItem90('x', dir); break;
            case 'y': e.preventDefault(); rotateItem90('y', dir); break;
            case 'z':
                if (!e.metaKey && !e.ctrlKey) { e.preventDefault(); rotateItem90('z', dir); }
                break;
            case 'delete': case 'backspace':
                if (selectedItem) { e.preventDefault(); deleteSelected(); } break;
            case 'escape': deselectItem(); break;
        }
    });
}

// ============================================
// Render Loop
// ============================================

function render() { renderer.render(scene, camera); }

function animate() {
    requestAnimationFrame(animate);
    orbitControls.update();
    render();
}

function onResize() {
    const container = document.getElementById('canvas-container');
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
    render();
}

// ============================================
// Start
// ============================================

init();
