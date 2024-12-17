// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

// Default theme values, default from dark theme of streamlit
let currentTheme = {
    primaryColor: "#FF4B4B",
    backgroundColor: "#0E1117",
    secondaryBackgroundColor: "#262730",
    textColor: "#FAFAFA",
    font: "sans serif"
};
let currentThemeString = JSON.stringify(currentTheme);
let newTheme = {}
let newThemeString = JSON.stringify(newTheme);
/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  // Run the code whenever theme changes
  try{
    newTheme = event.detail.theme;
    newThemeString = JSON.stringify(newTheme);
    if (currentThemeString !== newThemeString) { // If theme has changed
      console.log("Theme has changed, updating component")
      const renderData = event.detail; // This contains theme, disabled state, etc.
      if (!renderData) {
          console.error("No render data found")
      }
      sendValue(renderData.theme); // Send back the new theme
    }
  } catch (error) {
    console.error("Error occurred while updating theme")
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Set height to 0 to make sure the component is not visible
Streamlit.setFrameHeight(0)
