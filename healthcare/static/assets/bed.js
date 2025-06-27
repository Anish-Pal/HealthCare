document.addEventListener("DOMContentLoaded", function () {
    const areaFilter = document.getElementById("areaFilter");
    const bedTypeFilter = document.getElementById("bedTypeFilter");
    const hospitalFilter = document.getElementById("hospitalFilter");
    const hospitalCards = document.querySelectorAll(".hospital-card");
    
    function filterHospitals() {
        const selectedArea = areaFilter.value.toLowerCase();
        const selectedBedType = bedTypeFilter.value.toLowerCase();
        const selectedHospital = hospitalFilter.value.toLowerCase();

        hospitalCards.forEach(card => {
            const hospitalType = card.querySelector("p").textContent.toLowerCase();
            const bedDetails = card.querySelectorAll("p strong");
            let bedTypeMatch = selectedBedType === "all";

            bedDetails.forEach(detail => {
                if (detail.textContent.toLowerCase().includes(selectedBedType)) {
                    bedTypeMatch = true;
                }
            });

            if ((selectedArea === "all" || card.textContent.toLowerCase().includes(selectedArea)) &&
                (selectedHospital === "all" || hospitalType.includes(selectedHospital)) &&
                bedTypeMatch) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    }

    areaFilter.addEventListener("change", filterHospitals);
    bedTypeFilter.addEventListener("change", filterHospitals);
    hospitalFilter.addEventListener("change", filterHospitals);
});