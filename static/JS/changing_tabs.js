document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('[data-tab-target]');
    const tabContents = document.querySelectorAll('[data-tab-content]');
    const nextButton = document.getElementById('Next');

    nextButton.addEventListener('click', () => {
      const currentIndex = Array.from(tabs).findIndex(tab => tab.classList.contains('active'));
      const nextIndex = (currentIndex + 1) % tabs.length;
      toggleTabs(nextIndex);
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