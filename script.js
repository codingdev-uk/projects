// Science dataset with paragraphs, keywords, and reference links
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

// Helper function to render suggestions into the dropdown
function renderSuggestions(items) {
  suggestionBox.innerHTML = "";

  items.forEach(item => {
    const div = document.createElement("div");
    div.classList.add("suggestion-item");
    div.textContent = item.title;

    // Clicking a suggestion fills the box and displays the paragraph card
    div.addEventListener("click", function() {
      searchInput.value = item.keyword;
      suggestionBox.innerHTML = "";
      showPreviewCard(item);
    });

    suggestionBox.appendChild(div);
  });
}

// Helper function to display the content card with paragraph and link
function showPreviewCard(match) {
  previewContainer.innerHTML = `
    <div class="science-card">
      <h2>${match.title}</h2>
      <p>${match.paragraph}</p>
      <p>
        <a href="${match.url}" target="_blank">${match.linkText}</a>
      </p>
    </div>
  `;
}

// Helper function for partial character matches
function getMatches(inputVal) {
  const query = inputVal.toLowerCase().trim();
  if (!query) return scienceData; // Return all options if input is empty or spaces
  
  return scienceData.filter(item => 
    item.keyword.startsWith(query) || item.title.toLowerCase().includes(query)
  );
}

// Show all recommended options when the user clicks on the empty search box
searchInput.addEventListener("focus", function() {
  const matches = getMatches(this.value);
  renderSuggestions(matches);
});

// Update suggestions live as the user types (or clears the box)
searchInput.addEventListener("input", function() {
  const matches = getMatches(this.value);
  renderSuggestions(matches);
});

// Hide dropdown if the user clicks outside the search area
document.addEventListener("click", function(e) {
  if (!e.target.closest(".search-container")) {
    suggestionBox.innerHTML = "";
  }
});

// Handle pressing Enter
searchInput.addEventListener("keydown", function(e) {
  if (e.key === "Enter") {
    const matches = getMatches(this.value);
    suggestionBox.innerHTML = "";

    if (matches.length > 0 && this.value.trim() !== "") {
      showPreviewCard(matches[0]);
    } else if (this.value.trim() === "") {
      renderSuggestions(scienceData); // Keep showing options if Enter is pressed while empty
    } else {
      previewContainer.innerHTML = "<p>No matching science topics found.</p>";
    }
  }
});
