// Handle form submit and send data to Render backend
document.getElementById("riskForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const age = document.getElementById("age").value;
    const experience = document.getElementById("experience").value;

    fetch("https://ai-carrer-switch-risk-analyzer.onrender.com", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            age: age,
            experience: experience
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.getElementById("result").innerText =
            "Risk Level: " + data.risk;
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
