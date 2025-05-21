function showPage(pageId) {
    // Hide all pages
    const pages = document.querySelectorAll('.page');
    pages.forEach(page => {
      page.classList.remove('active');
    });function showPage(pageId) {
        // Hide all pages
        const pages = document.querySelectorAll('.page');
        pages.forEach(page => {
          page.classList.remove('active');
        });
      
        // Show the selected page
        const selectedPage = document.getElementById(pageId);
        if (selectedPage) {
          selectedPage.classList.add('active');
        }
      }
      
      // Show the home page by default
      showPage('home');
      
  
    // Show the selected page
    const selectedPage = document.getElementById(pageId);
    if (selectedPage) {
      selectedPage.classList.add('active');
    }
  }
  
  // Show the home page by default
  showPage('home');
  
