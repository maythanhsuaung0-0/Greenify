document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('[data-tab-target]');
    const tabContents = document.querySelectorAll('[data-tab-content]');
    const nextButton = document.getElementById('Next');

    nextButton.addEventListener('click', () => {
      const currentIndex = Array.from(tabs).findIndex(tab => tab.classList.contains('active')); // Finds the index of the currently active tab among a collection of tabs
      const nextIndex = (currentIndex + 1) % tabs.length; // Calculates the index of the next tab by incrementing the current index by 1
      toggleTabs(nextIndex); //Purpose of this function is to switch the active tab based on the index provided
    });

  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => {
      toggleTabs(index);
    });
  });

  function toggleTabs(activeIndex) {
    tabs.forEach((tab, i) => {
      const isActive = i === activeIndex;
      tab.classList.toggle('active', isActive);
      tab.classList.toggle('inactive', !isActive);
      tabContents[i].classList.toggle('active', isActive);
      tabContents[i].classList.toggle('inactive', !isActive);
    });
  }
});