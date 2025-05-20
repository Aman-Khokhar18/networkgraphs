const uploadBtn = document.getElementById("uploadBtn");
const fileInput = document.getElementById("fileInput");
const statusDiv = document.getElementById("status");

uploadBtn.addEventListener("click", async () => {
  if (!fileInput.files.length) {
    alert("Please choose a file");
    return;
  }
  uploadBtn.disabled = true;
  statusDiv.textContent = "Uploading…";
  const form = new FormData();
  form.append("file", fileInput.files[0]);

  try {
    const res = await fetch("/api/extract-graph", {
      method: "POST",
      body: form
    });
    if (!res.ok) throw new Error(await res.text());
    const graph = await res.json();
    statusDiv.textContent = `Got ${graph.nodes.length} nodes, ${graph.edges.length} edges`;
    renderGraph(graph);
  } catch (err) {
    statusDiv.textContent = "Error: " + err.message;
  } finally {
    uploadBtn.disabled = false;
  }
});

function renderGraph({ nodes, edges }) {
  // 1) Collect unique node types in the order they appear
  const types = Array.from(new Set(nodes.map(n => n.type)));

  // 2) Define a reusable palette of colors
  const palette = [
    '#FF6B6B',  // coral
    '#4ECDC4',  // teal
    '#1A535C',  // dark blue
    '#FFE66D',  // yellow
    '#E67E22',  // orange
    '#9B59B6',  // purple
    '#3498DB',  // sky-blue
    '#F39C12',  // gold
    '#2ECC71',  // green
    '#E74C3C',  // red
  ];

  // 3) Build a style rule per type, cycling through the palette
  const typeStyles = types.map((type, i) => ({
    selector: `node[type = "${type}"]`,
    style: {
      'background-color': palette[i % palette.length]
    }
  }));

  // 4) Initialize Cytoscape with your base styles + these dynamic ones
  cytoscape({
    container: document.getElementById("cy"),
    elements: [
      ...nodes.map(n => ({ data: { id: n.id, label: n.label, type: n.type } })),
      ...edges.map(e => ({ data: { source: e.source, target: e.target, label: e.label } }))
    ],
    style: [
      // Base node styling (auto-size, wrap, dark grey text, etc.)
      {
        selector: 'node',
        style: {
          'label': 'data(label)',
          'text-valign': 'center',
          'text-halign': 'center',
          'text-wrap': 'wrap',
          'text-max-width': '80px',
          'background-color': '#67a',    // fallback color
          'color': '#333333',            // dark grey label
          'font-size': 10,
          'padding': '10px',
          'shape': 'ellipse',
          'width': 'label',
          'height': 'label',
          'min-width': '40px',
          'min-height': '40px'
        }
      },
      // Insert our dynamically generated type→color rules
      ...typeStyles,
      // Edge styling (keep as is)
      {
        selector: 'edge',
        style: {
          'label': 'data(label)',
          'curve-style': 'bezier',
          'target-arrow-shape': 'triangle',
          'font-size': 8,
          'line-color': '#bbb',
          'target-arrow-color': '#bbb'
        }
      }
    ],
    layout: { name: "cose" }
  });
}


