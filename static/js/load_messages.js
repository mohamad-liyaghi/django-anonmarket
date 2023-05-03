function loadMore() {
    // Get current 'to' and 'from' values from query parameters, or set them to default values
    let searchParams = new URLSearchParams(window.location.search);
    let from = parseInt(searchParams.get('from')) || 0;
    let to = parseInt(searchParams.get('to')) || 20;
  
    // Increase both 'to' and 'from' values by 20
    from += 20;
    to += 20;
  
    // Update query parameters in URL
    searchParams.set('from', from.toString());
    searchParams.set('to', to.toString());
    window.location.search = searchParams.toString();
  }