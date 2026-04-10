import { useState, useRef, useEffect } from "react";
import * as THREE from "three";

// 25 Seacove Drive — As-Built 3D Model
// Dimensions extracted from Douglas W. Rucker AIA original blueprints (1958)
// Plus 1960 bedroom addition and garage addition

const COLORS = {
  walls: 0xE8DCC8,        // warm stucco/plaster
  roof: 0x8B7355,         // wood/comp roof
  beams: 0x8B6914,        // exposed Douglas fir beams
  posts: 0x8B6914,        // exposed posts
  glass: 0x87CEEB,        // window glass
  foundation: 0x999999,   // concrete
  ground: 0x7CAF5A,       // grass
  driveway: 0xAAAAAA,     // concrete driveway
  pool: 0x4A90D9,         // pool water
  poolDeck: 0xCCC0A8,     // pool deck
  door: 0x654321,         // wood doors
  terrain: 0x6B8E4E,      // hillside
  road: 0x555555,         // road surface
};

export default function SeacoveModel() {
  const mountRef = useRef(null);
  const [info, setInfo] = useState("Click and drag to rotate. Scroll to zoom. Right-click drag to pan.");
  const [viewMode, setViewMode] = useState("perspective");

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const width = container.clientWidth;
    const height = container.clientHeight;

    // Scene setup
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xD4E6F1);
    scene.fog = new THREE.Fog(0xD4E6F1, 200, 500);

    // Camera
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(80, 50, 90);
    camera.lookAt(0, 5, 0);

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // Lighting — warm Southern California sun
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xFFF5E0, 0.8);
    sunLight.position.set(50, 80, 30);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 2048;
    sunLight.shadow.mapSize.height = 2048;
    sunLight.shadow.camera.near = 0.5;
    sunLight.shadow.camera.far = 300;
    sunLight.shadow.camera.left = -100;
    sunLight.shadow.camera.right = 100;
    sunLight.shadow.camera.top = 100;
    sunLight.shadow.camera.bottom = -100;
    scene.add(sunLight);

    const fillLight = new THREE.DirectionalLight(0xB0C4DE, 0.3);
    fillLight.position.set(-30, 40, -20);
    scene.add(fillLight);

    // Helper functions
    function box(w, h, d, color, x, y, z) {
      const geo = new THREE.BoxGeometry(w, h, d);
      const mat = new THREE.MeshLambertMaterial({ color });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(x, y, z);
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      return mesh;
    }

    function makeRoof(points, height, color) {
      const shape = new THREE.Shape();
      shape.moveTo(points[0][0], points[0][1]);
      for (let i = 1; i < points.length; i++) {
        shape.lineTo(points[i][0], points[i][1]);
      }
      shape.lineTo(points[0][0], points[0][1]);

      const geo = new THREE.ExtrudeGeometry(shape, { depth: 0.3, bevelEnabled: false });
      const mat = new THREE.MeshLambertMaterial({ color });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.rotation.x = -Math.PI / 2;
      mesh.position.y = height;
      mesh.castShadow = true;
      mesh.receiveShadow = true;
      return mesh;
    }

    // ========================================
    // SITE — Ground plane and terrain
    // ========================================
    const siteGroup = new THREE.Group();
    siteGroup.name = "Site";

    // Ground
    const groundGeo = new THREE.PlaneGeometry(300, 300);
    const groundMat = new THREE.MeshLambertMaterial({ color: COLORS.ground });
    const ground = new THREE.Mesh(groundGeo, groundMat);
    ground.rotation.x = -Math.PI / 2;
    ground.position.y = -0.1;
    ground.receiveShadow = true;
    siteGroup.add(ground);

    // Sea Cove Drive (curved road at front of property)
    const roadGeo = new THREE.PlaneGeometry(20, 180);
    const roadMat = new THREE.MeshLambertMaterial({ color: COLORS.road });
    const road = new THREE.Mesh(roadGeo, roadMat);
    road.rotation.x = -Math.PI / 2;
    road.position.set(-55, 0.01, 0);
    road.receiveShadow = true;
    siteGroup.add(road);

    // Clipper Road (perpendicular)
    const road2Geo = new THREE.PlaneGeometry(180, 16);
    const road2Mat = new THREE.MeshLambertMaterial({ color: COLORS.road });
    const road2 = new THREE.Mesh(road2Geo, road2Mat);
    road2.rotation.x = -Math.PI / 2;
    road2.position.set(0, 0.01, 65);
    road2.receiveShadow = true;
    siteGroup.add(road2);

    // Driveway
    const driveGeo = new THREE.PlaneGeometry(12, 25);
    const driveMat = new THREE.MeshLambertMaterial({ color: COLORS.driveway });
    const drive = new THREE.Mesh(driveGeo, driveMat);
    drive.rotation.x = -Math.PI / 2;
    drive.position.set(-35, 0.05, 30);
    drive.receiveShadow = true;
    siteGroup.add(drive);

    // Gentle hillside terrain rising to the north
    for (let i = 0; i < 5; i++) {
      const hillGeo = new THREE.PlaneGeometry(250, 40);
      const hillMat = new THREE.MeshLambertMaterial({ color: i % 2 === 0 ? COLORS.terrain : COLORS.ground });
      const hill = new THREE.Mesh(hillGeo, hillMat);
      hill.rotation.x = -Math.PI / 2 + 0.15;
      hill.position.set(20, i * 2 + 1, -60 - i * 30);
      hill.receiveShadow = true;
      siteGroup.add(hill);
    }

    scene.add(siteGroup);

    // ========================================
    // MAIN HOUSE — Original 1958 Rucker design
    // Approx 60' long x 28' deep, L-shape
    // ========================================
    const houseGroup = new THREE.Group();
    houseGroup.name = "Original_House_1958";

    // Wall height: 8' plate
    const plateH = 8;
    const wallThick = 0.5;

    // === LIVING WING (west portion) ===
    // Living room + dining + entry — approx 30' x 18'
    const livingW = 30;
    const livingD = 18;

    // South wall (front)
    houseGroup.add(box(livingW, plateH, wallThick, COLORS.walls, -livingW/2 + 15, plateH/2, livingD/2));
    // North wall
    houseGroup.add(box(livingW, plateH, wallThick, COLORS.walls, -livingW/2 + 15, plateH/2, -livingD/2));
    // West wall
    houseGroup.add(box(wallThick, plateH, livingD, COLORS.walls, -livingW + 15, plateH/2, 0));

    // Glass walls — south face of living room (floor to ceiling between posts)
    for (let i = 0; i < 4; i++) {
      const glassGeo = new THREE.PlaneGeometry(6, 7);
      const glassMat = new THREE.MeshLambertMaterial({ color: COLORS.glass, transparent: true, opacity: 0.3, side: THREE.DoubleSide });
      const glass = new THREE.Mesh(glassGeo, glassMat);
      glass.position.set(-12 + i * 7, 4, livingD/2 - 0.1);
      houseGroup.add(glass);
    }

    // === BEDROOM WING (east portion) ===
    // 3 bedrooms + baths — approx 32' x 24'
    const bedW = 32;
    const bedD = 24;
    const bedOffsetX = livingW/2 + 15;

    // South wall
    houseGroup.add(box(bedW, plateH, wallThick, COLORS.walls, bedOffsetX - bedW/2 + bedW/2 - 1, plateH/2, bedD/2));
    // North wall
    houseGroup.add(box(bedW, plateH, wallThick, COLORS.walls, bedOffsetX - bedW/2 + bedW/2 - 1, plateH/2, -bedD/2 + 3));
    // East wall
    houseGroup.add(box(wallThick, plateH, bedD - 3, COLORS.walls, bedOffsetX + bedW/2 - 2, plateH/2, (bedD/2 + (-bedD/2 + 3))/2));

    // Interior walls (simplified)
    // Hall wall
    houseGroup.add(box(bedW - 4, plateH, wallThick, COLORS.walls, bedOffsetX + bedW/4 - 2, plateH/2, 3));
    // Bedroom dividers
    houseGroup.add(box(wallThick, plateH, 8, COLORS.walls, bedOffsetX + 6, plateH/2, 7.5));
    houseGroup.add(box(wallThick, plateH, 8, COLORS.walls, bedOffsetX + 16, plateH/2, 7.5));

    // Windows on bedroom wing — east face
    for (let i = 0; i < 3; i++) {
      const winGeo = new THREE.PlaneGeometry(5, 4);
      const winMat = new THREE.MeshLambertMaterial({ color: COLORS.glass, transparent: true, opacity: 0.3, side: THREE.DoubleSide });
      const win = new THREE.Mesh(winGeo, winMat);
      win.position.set(bedOffsetX + bedW/2 - 1.9, 5, -bedD/4 + i * 6);
      win.rotation.y = Math.PI / 2;
      houseGroup.add(win);
    }

    // === EXPOSED POST AND BEAM STRUCTURE ===
    const postSize = 0.33; // 4x4 posts

    // Posts along south face (living area)
    for (let i = 0; i < 5; i++) {
      const post = box(postSize, plateH, postSize, COLORS.posts, -14 + i * 7, plateH/2, livingD/2);
      houseGroup.add(post);
    }

    // Main ridge beam
    houseGroup.add(box(livingW + 6, 0.66, 0.5, COLORS.beams, -livingW/2 + 18, plateH + 0.33, 0));

    // Cross beams (exposed rafters at living room)
    for (let i = 0; i < 8; i++) {
      houseGroup.add(box(0.33, 0.5, livingD + 6, COLORS.beams, -14 + i * 4, plateH - 0.25, 0));
    }

    // Beam across bedroom wing
    houseGroup.add(box(bedW + 4, 0.66, 0.5, COLORS.beams, bedOffsetX + bedW/4 - 2, plateH + 0.33, 3));

    // === ROOF — Low pitch with generous overhangs ===
    const overhang = 3.5;

    // Living wing roof
    const livingRoof = makeRoof([
      [-livingW - overhang + 15, -livingD/2 - overhang],
      [overhang + 15, -livingD/2 - overhang],
      [overhang + 15, livingD/2 + overhang],
      [-livingW - overhang + 15, livingD/2 + overhang],
    ], plateH + 1.5, COLORS.roof);
    houseGroup.add(livingRoof);

    // Bedroom wing roof
    const bedRoof = makeRoof([
      [bedOffsetX - bedW/2 - overhang + bedW/2 - 3, -bedD/2 + 3 - overhang],
      [bedOffsetX + bedW/2 + overhang - 2, -bedD/2 + 3 - overhang],
      [bedOffsetX + bedW/2 + overhang - 2, bedD/2 + overhang],
      [bedOffsetX - bedW/2 - overhang + bedW/2 - 3, bedD/2 + overhang],
    ], plateH + 1.2, COLORS.roof);
    houseGroup.add(bedRoof);

    // === FRONT DOOR ===
    houseGroup.add(box(3.5, 7, 0.3, COLORS.door, 2, 3.5, livingD/2 + 0.3));

    scene.add(houseGroup);

    // ========================================
    // 1960 BEDROOM ADDITION
    // 2 bedrooms + hall + bath — approx 25' x 14'
    // Added to rear (north) of house
    // ========================================
    const additionGroup = new THREE.Group();
    additionGroup.name = "Bedroom_Addition_1960";

    const addW = 25;
    const addD = 14;
    const addX = 15;
    const addZ = -livingD/2 - addD/2;

    // Walls
    houseGroup.add(box(addW, plateH, wallThick, COLORS.walls, addX, plateH/2, addZ - addD/2)); // north
    houseGroup.add(box(wallThick, plateH, addD, COLORS.walls, addX - addW/2, plateH/2, addZ)); // west
    houseGroup.add(box(wallThick, plateH, addD, COLORS.walls, addX + addW/2, plateH/2, addZ)); // east

    // Interior divider
    houseGroup.add(box(wallThick, plateH, addD - 2, COLORS.walls, addX + 2, plateH/2, addZ));

    // Windows
    for (let i = 0; i < 2; i++) {
      const winGeo = new THREE.PlaneGeometry(6, 4);
      const winMat = new THREE.MeshLambertMaterial({ color: COLORS.glass, transparent: true, opacity: 0.3, side: THREE.DoubleSide });
      const win = new THREE.Mesh(winGeo, winMat);
      win.position.set(addX - 8 + i * 18, 5, addZ - addD/2 - 0.1);
      additionGroup.add(win);
    }

    // Roof
    const addRoof = makeRoof([
      [addX - addW/2 - overhang, addZ - addD/2 - overhang],
      [addX + addW/2 + overhang, addZ - addD/2 - overhang],
      [addX + addW/2 + overhang, addZ + addD/2 + 1],
      [addX - addW/2 - overhang, addZ + addD/2 + 1],
    ], plateH + 0.8, COLORS.roof);
    additionGroup.add(addRoof);

    scene.add(additionGroup);

    // ========================================
    // GARAGE (Addition, later date)
    // Approx 20' x 20'
    // ========================================
    const garageGroup = new THREE.Group();
    garageGroup.name = "Garage_Addition";

    const garW = 20;
    const garD = 20;
    const garX = 40;
    const garZ = 15;

    garageGroup.add(box(garW, plateH, wallThick, COLORS.walls, garX, plateH/2, garZ + garD/2)); // south
    garageGroup.add(box(garW, plateH, wallThick, COLORS.walls, garX, plateH/2, garZ - garD/2)); // north
    garageGroup.add(box(wallThick, plateH, garD, COLORS.walls, garX + garW/2, plateH/2, garZ)); // east
    // West wall (connects to house) — partial, has door opening
    garageGroup.add(box(wallThick, plateH, 7, COLORS.walls, garX - garW/2, plateH/2, garZ + 6.5));
    garageGroup.add(box(wallThick, plateH, 5, COLORS.walls, garX - garW/2, plateH/2, garZ - 7.5));

    // Garage door (south face)
    const garageDoorGeo = new THREE.PlaneGeometry(16, 7);
    const garageDoorMat = new THREE.MeshLambertMaterial({ color: 0xAA9977, side: THREE.DoubleSide });
    const garageDoor = new THREE.Mesh(garageDoorGeo, garageDoorMat);
    garageDoor.position.set(garX, 3.5, garZ + garD/2 + 0.1);
    garageGroup.add(garageDoor);

    // Garage roof
    const garRoof = makeRoof([
      [garX - garW/2 - overhang, garZ - garD/2 - overhang],
      [garX + garW/2 + overhang, garZ - garD/2 - overhang],
      [garX + garW/2 + overhang, garZ + garD/2 + overhang],
      [garX - garW/2 - overhang, garZ + garD/2 + overhang],
    ], plateH + 0.6, COLORS.roof);
    garageGroup.add(garRoof);

    scene.add(garageGroup);

    // ========================================
    // POOL — West side of house
    // ========================================
    const poolGroup = new THREE.Group();
    poolGroup.name = "Pool";

    // Pool deck
    const deckGeo = new THREE.PlaneGeometry(22, 16);
    const deckMat = new THREE.MeshLambertMaterial({ color: COLORS.poolDeck });
    const deck = new THREE.Mesh(deckGeo, deckMat);
    deck.rotation.x = -Math.PI / 2;
    deck.position.set(-25, 0.15, 20);
    deck.receiveShadow = true;
    poolGroup.add(deck);

    // Pool water
    const poolGeo = new THREE.BoxGeometry(16, 1.5, 10);
    const poolMat = new THREE.MeshLambertMaterial({ color: COLORS.pool, transparent: true, opacity: 0.7 });
    const pool = new THREE.Mesh(poolGeo, poolMat);
    pool.position.set(-25, -0.5, 20);
    poolGroup.add(pool);

    // Pool edge
    const edgeGeo = new THREE.BoxGeometry(17, 0.4, 11);
    const edgeMat = new THREE.MeshLambertMaterial({ color: COLORS.poolDeck });
    const edge = new THREE.Mesh(edgeGeo, edgeMat);
    edge.position.set(-25, 0.2, 20);
    poolGroup.add(edge);

    scene.add(poolGroup);

    // ========================================
    // LANDSCAPE — Palm trees (as in original rendering)
    // ========================================
    const treeGroup = new THREE.Group();
    treeGroup.name = "Landscape";

    function palmTree(x, z, height) {
      // Trunk
      const trunkGeo = new THREE.CylinderGeometry(0.3, 0.5, height, 8);
      const trunkMat = new THREE.MeshLambertMaterial({ color: 0x8B7355 });
      const trunk = new THREE.Mesh(trunkGeo, trunkMat);
      trunk.position.set(x, height / 2, z);
      trunk.castShadow = true;
      treeGroup.add(trunk);

      // Crown (simplified as a sphere)
      const crownGeo = new THREE.SphereGeometry(4, 8, 6);
      const crownMat = new THREE.MeshLambertMaterial({ color: 0x228B22 });
      const crown = new THREE.Mesh(crownGeo, crownMat);
      crown.position.set(x, height + 2, z);
      crown.castShadow = true;
      treeGroup.add(crown);
    }

    // Palm trees (matching the original rendering placement)
    palmTree(-5, -5, 25);
    palmTree(5, -15, 28);
    palmTree(-20, 5, 22);
    palmTree(35, -20, 26);
    palmTree(-40, 30, 20);

    // Smaller landscaping trees
    function shrub(x, z, size) {
      const geo = new THREE.SphereGeometry(size, 6, 5);
      const mat = new THREE.MeshLambertMaterial({ color: 0x2E8B2E });
      const mesh = new THREE.Mesh(geo, mat);
      mesh.position.set(x, size, z);
      mesh.castShadow = true;
      treeGroup.add(mesh);
    }

    shrub(-38, 12, 2);
    shrub(-30, 35, 1.5);
    shrub(50, 30, 2);
    shrub(55, -10, 1.8);
    shrub(-10, 25, 1.5);
    shrub(20, 25, 2);

    scene.add(treeGroup);

    // ========================================
    // LABELS
    // ========================================

    // Simple orbit controls implementation
    let isDragging = false;
    let isRightDrag = false;
    let prevMouse = { x: 0, y: 0 };
    let spherical = { theta: Math.PI / 4, phi: Math.PI / 4, radius: 120 };
    let target = new THREE.Vector3(10, 4, 5);

    function updateCamera() {
      camera.position.x = target.x + spherical.radius * Math.sin(spherical.phi) * Math.cos(spherical.theta);
      camera.position.y = target.y + spherical.radius * Math.cos(spherical.phi);
      camera.position.z = target.z + spherical.radius * Math.sin(spherical.phi) * Math.sin(spherical.theta);
      camera.lookAt(target);
    }
    updateCamera();

    const onMouseDown = (e) => {
      isDragging = true;
      isRightDrag = e.button === 2;
      prevMouse = { x: e.clientX, y: e.clientY };
    };
    const onMouseMove = (e) => {
      if (!isDragging) return;
      const dx = e.clientX - prevMouse.x;
      const dy = e.clientY - prevMouse.y;

      if (isRightDrag) {
        const panSpeed = 0.15;
        const right = new THREE.Vector3();
        const up = new THREE.Vector3(0, 1, 0);
        right.crossVectors(camera.getWorldDirection(new THREE.Vector3()), up).normalize();
        target.add(right.multiplyScalar(-dx * panSpeed));
        target.y += dy * panSpeed;
      } else {
        spherical.theta -= dx * 0.005;
        spherical.phi = Math.max(0.1, Math.min(Math.PI / 2 - 0.01, spherical.phi + dy * 0.005));
      }

      prevMouse = { x: e.clientX, y: e.clientY };
      updateCamera();
    };
    const onMouseUp = () => { isDragging = false; isRightDrag = false; };
    const onWheel = (e) => {
      spherical.radius = Math.max(20, Math.min(250, spherical.radius + e.deltaY * 0.1));
      updateCamera();
    };
    const onContextMenu = (e) => e.preventDefault();

    renderer.domElement.addEventListener("mousedown", onMouseDown);
    renderer.domElement.addEventListener("mousemove", onMouseMove);
    renderer.domElement.addEventListener("mouseup", onMouseUp);
    renderer.domElement.addEventListener("wheel", onWheel);
    renderer.domElement.addEventListener("contextmenu", onContextMenu);

    // Animation
    let animId;
    const animate = () => {
      animId = requestAnimationFrame(animate);
      renderer.render(scene, camera);
    };
    animate();

    // Resize handler
    const handleResize = () => {
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };
    window.addEventListener("resize", handleResize);

    // Preset views
    window.__seacoveSetView = (view) => {
      if (view === "aerial") {
        spherical = { theta: Math.PI / 4, phi: 0.4, radius: 140 };
        target.set(10, 0, 5);
      } else if (view === "south") {
        spherical = { theta: Math.PI / 2, phi: Math.PI / 3, radius: 80 };
        target.set(10, 4, 0);
      } else if (view === "east") {
        spherical = { theta: 0, phi: Math.PI / 3, radius: 80 };
        target.set(10, 4, 0);
      } else if (view === "north") {
        spherical = { theta: -Math.PI / 2, phi: Math.PI / 3, radius: 80 };
        target.set(10, 4, 0);
      } else if (view === "west") {
        spherical = { theta: Math.PI, phi: Math.PI / 3, radius: 80 };
        target.set(10, 4, 0);
      } else if (view === "rendering") {
        spherical = { theta: Math.PI / 3.5, phi: 0.5, radius: 110 };
        target.set(5, 2, 10);
      }
      updateCamera();
    };

    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", handleResize);
      renderer.domElement.removeEventListener("mousedown", onMouseDown);
      renderer.domElement.removeEventListener("mousemove", onMouseMove);
      renderer.domElement.removeEventListener("mouseup", onMouseUp);
      renderer.domElement.removeEventListener("wheel", onWheel);
      renderer.domElement.removeEventListener("contextmenu", onContextMenu);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  const setView = (view) => {
    if (window.__seacoveSetView) window.__seacoveSetView(view);
    const labels = {
      aerial: "Aerial view — similar to Rucker's 1958 presentation rendering",
      south: "South Elevation — front of house on Sea Cove Drive",
      east: "East Elevation — bedroom wing",
      north: "North Elevation — rear, showing 1960 addition",
      west: "West Elevation — living wing and pool",
      rendering: "Rendering angle — matching the original Rucker presentation drawing",
    };
    setInfo(labels[view] || "");
  };

  return (
    <div style={{ width: "100%", height: "100vh", display: "flex", flexDirection: "column", background: "#1a1a2e", fontFamily: "Arial, sans-serif" }}>
      {/* Header */}
      <div style={{ padding: "12px 20px", background: "#1B3A5C", color: "white", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <span style={{ fontSize: "16px", fontWeight: "bold" }}>25 Sea Cove Drive — As-Built 3D Model</span>
          <span style={{ fontSize: "12px", marginLeft: "16px", opacity: 0.7 }}>Douglas W. Rucker AIA, 1958 | Rancho Palos Verdes, CA</span>
        </div>
        <div style={{ fontSize: "11px", opacity: 0.6 }}>RPV Permit Architect</div>
      </div>

      {/* View buttons */}
      <div style={{ padding: "8px 20px", background: "#243B55", display: "flex", gap: "8px", flexWrap: "wrap", alignItems: "center" }}>
        <span style={{ color: "#8899AA", fontSize: "11px", marginRight: "4px" }}>VIEWS:</span>
        {["rendering", "aerial", "south", "east", "north", "west"].map(v => (
          <button
            key={v}
            onClick={() => setView(v)}
            style={{
              padding: "4px 12px", border: "1px solid #4A6A8A", borderRadius: "3px",
              background: "transparent", color: "#AAC4DD", fontSize: "11px", cursor: "pointer",
              textTransform: "capitalize"
            }}
            onMouseOver={e => { e.target.style.background = "#1B3A5C"; }}
            onMouseOut={e => { e.target.style.background = "transparent"; }}
          >
            {v === "rendering" ? "Rucker Rendering" : v + " Elev."}
          </button>
        ))}
      </div>

      {/* 3D viewport */}
      <div ref={mountRef} style={{ flex: 1, cursor: "grab" }} />

      {/* Info bar */}
      <div style={{ padding: "8px 20px", background: "#1B3A5C", color: "#8899AA", fontSize: "11px", display: "flex", justifyContent: "space-between" }}>
        <span>{info}</span>
        <span>Dimensions from original 1958 blueprints + 1960 addition + garage addition | Approx. scale</span>
      </div>

      {/* Legend */}
      <div style={{ padding: "8px 20px", background: "#0F2136", display: "flex", gap: "20px", flexWrap: "wrap" }}>
        {[
          { color: "#E8DCC8", label: "Original House (1958)" },
          { color: "#8B7355", label: "Roof / Overhangs" },
          { color: "#8B6914", label: "Exposed Beams & Posts" },
          { color: "#87CEEB", label: "Glass / Windows" },
          { color: "#4A90D9", label: "Pool" },
          { color: "#7CAF5A", label: "Landscape" },
        ].map(({ color, label }) => (
          <div key={label} style={{ display: "flex", alignItems: "center", gap: "6px" }}>
            <div style={{ width: "12px", height: "12px", background: color, borderRadius: "2px" }} />
            <span style={{ color: "#8899AA", fontSize: "10px" }}>{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
