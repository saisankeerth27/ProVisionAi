document.getElementById("uploadForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const fileInput = document.getElementById("imageInput");
  const resultContainer = document.getElementById("result");
  const imageElement = document.getElementById("uploadedImage");
  const annotationText = document.getElementById("annotationText");

  if (fileInput.files.length === 0) {
      alert("Please select an image to upload.");
      return;
  }

  // Create a FormData object to send the file
  const formData = new FormData();
  formData.append("image", fileInput.files[0]);

  try {
      // Display uploaded image immediately
      imageElement.src = URL.createObjectURL(fileInput.files[0]);
      imageElement.style.display = "block";
      annotationText.innerText = "Processing annotation..."; // Placeholder text
      resultContainer.style.display = "flex"; // Show result container

      // Send image to backend
      const response = await fetch("/annotate", {
          method: "POST",
          body: formData,
      });

      const data = await response.json();

      if (data.success) {
          annotationText.innerText = data.annotation; // Display AI-generated annotation
      } else {
          annotationText.innerText = "Error: " + data.message;
      }
  } catch (error) {
      console.error("Error:", error);
      annotationText.innerText = "An error occurred while processing the image.";
  }
});