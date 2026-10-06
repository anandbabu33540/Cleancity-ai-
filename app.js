const API_BASE_URL = "http://127.0.0.1:8000/api";

// 1. Fetch Dashboard Stats
async function fetchDashboardStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard/stats`);
        const data = await response.json();
        document.getElementById('total-reports').innerText = data.total_reports || 0;
        document.getElementById('pending-reports').innerText = data.pending_reports || 0;
        document.getElementById('resolved-reports').innerText = data.resolved_reports || 0;
    } catch (error) {
        console.error("Error fetching stats:", error);
    }
}

// 2. Fetch Hotspots List
async function fetchHotspots() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard/hotspots`);
        const result = await response.json();
        const tbody = document.getElementById('hotspotsTable');
        tbody.innerHTML = ""; 
        
        result.data.forEach(hotspot => {
            tbody.innerHTML += `
                <tr>
                    <td>Ward ID: ${hotspot.ward_id}</td>
                    <td>${hotspot.latitude}</td>
                    <td>${hotspot.longitude}</td>
                    <td>${hotspot.report_count}</td>
                    <td><b style="color: ${hotspot.severity_level === 'high' ? 'red' : 'orange'}">${hotspot.severity_level}</b></td>
                </tr>
            `;
        });
    } catch (error) {
        console.error("Error fetching hotspots:", error);
    }
}

// 3. Submit Report & AI Analysis
const reportForm = document.getElementById('reportForm');
if(reportForm) {
    reportForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const statusMsg = document.getElementById('statusMsg');
        statusMsg.innerText = "Submitting report and running AI model... Please wait.";

        // For demo purposes, we will mock the user and ward IDs
        const dummyUserId = "00000000-0000-0000-0000-000000000001"; // Need real UUID in prod
        const dummyWardId = "00000000-0000-0000-0000-000000000001"; 
        const latlng = document.getElementById('latlng').value.split(',');

        const reportData = {
            user_id: dummyUserId,
            ward_id: dummyWardId,
            latitude: parseFloat(latlng[0]),
            longitude: parseFloat(latlng[1]),
            description: document.getElementById('desc').value,
            image_url: "dummy-url-for-now.jpg" // In real app, upload to Supabase Storage first
        };

        try {
            // Step 1: Create Report
            const createRes = await fetch(`${API_BASE_URL}/reports/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(reportData)
            });
            const createdData = await createRes.json();
            
            if(createRes.ok) {
                statusMsg.innerText = "Report created! AI Analysis running...";
                statusMsg.style.color = "blue";
                
                // Step 2: Upload File for AI Analysis
                const fileInput = document.getElementById('imageFile');
                const formData = new FormData();
                formData.append("file", fileInput.files[0]);

                const aiRes = await fetch(`${API_BASE_URL}/reports/${createdData.data.id}/analyze`, {
                    method: 'POST',
                    body: formData
                });
                const aiResult = await aiRes.json();
                
                if(aiRes.ok) {
                    statusMsg.innerText = `Success! AI Detected: ${aiResult.analysis.predicted_class} (Confidence: ${aiResult.analysis.confidence})`;
                    statusMsg.style.color = "green";
                    reportForm.reset();
                }
            } else {
                statusMsg.innerText = "Error creating report.";
                statusMsg.style.color = "red";
            }
        } catch (error) {
            console.error("Submit Error:", error);
            statusMsg.innerText = "Backend connection failed. Is FastAPI running?";
            statusMsg.style.color = "red";
        }
    });
}
