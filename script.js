// Science dataset with paragraphs, keywords, and reference links
const scienceData = [
  {
    keyword: "static electricity",
    title: "Static Electricity",
    paragraph: "Static electricity is an imbalance of electric charges within or on the surface of a material. It builds up until it is able to move away by means of a discharge or current.",
    linkText: "Learn more about Static Electricity charges",
    url: "https://en.wikipedia.org/wiki/Static_electricity"
  },
  {
    keyword: "resistance",
    title: "Electrical Resistance",
    paragraph: "Electrical resistance is a measure of the opposition to current flow in an electrical circuit. Resistance is measured in ohms, symbolized by the Greek letter omega (Ω).",
    linkText: "Explore Electrical Resistance details",
    url: "https://en.wikipedia.org/wiki/Electrical_resistance_and_conductance"
  },
  {
    keyword: "conductivity",
    title: "Electrical Conductivity",
    paragraph: "Conductivity is a material's ability to conduct an electric current. Materials that have high conductivity, like copper and aluminum, allow electricity to pass through them very easily.",
    linkText: "Read more about Conductivity",
    url: "https://en.wikipedia.org/wiki/Electrical_resistivity_and_conductivity"
  },
  {
    keyword: "insulators",
    title: "Electrical Insulators",
    paragraph: "Insulators are materials that prevent the free flow of electrons from atom to atom and molecule to molecule. Common examples include rubber, glass, plastic, and dry air.",
    linkText: "Discover how Insulators block current",
    url: "https://en.wikipedia.org/wiki/Insulator_(electricity)"
  }
];

const searchInput = document.getElementById("search-input");
const suggestionBox = document.getElementById("suggestion-box");
const previewContainer = document.getElementById("preview-container");

// Helper function for partial character matches (e.g., s, st, sta, static...)
function getMatches(inputVal) {
  const query = inputVal.toLowerCase().trim();
  if (!query) return [];
  return scienceData.filter(item => {
    for (let i = 1; i <= item.keyword.length; i++) {
      if (item.keyword.substring(0, i) === query) {
        return true;
      }
    }
    return false;
  });
}

// Event listener for live typing (Dropdown Suggestions)
searchInput.addEventListener("input", function() {
  const matches = getMatches(this.value);
  suggestionBox.innerHTML = "";

  if (matches.length > 0 && this.value.trim() !== "") {
    matches.forEach(match => {
      const div = document.createElement("div");
      div.classList.add("suggestion-item");
      div.textContent = match.title;

      // Clicking dropdown suggestion opens the external link directly
      div.addEventListener("click", function() {
        window.open(match.url, "_blank");
      });
      suggestionBox.appendChild(div);
    });
  }
});

// Event listener for pressing Enter (Renders the content card with paragraph and link)
searchInput.addEventListener("keydown", function(e) {
  if (e.key === "Enter") {
    const matches = getMatches(this.value);
    suggestionBox.innerHTML = ""; // Clear suggestions dropdown

    if (matches.length > 0) {
      const match = matches[0]; // Take top match
      
      previewContainer.innerHTML = `
        <div class="science-card">
          <h2>${match.title}</h2>
          <p>${match.paragraph}</p>
          <p>
            <a href="${match.url}" target="_blank">${match.linkText}</a>
          </p>
        </div>
      `;
    } else {
      previewContainer.innerHTML = "<p>No matching science topics found.</p>";
    }
  }
});
