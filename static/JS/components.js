function setConfirmDeleteInfo(id, name,url) {
    console.log("setConfirmDeleteInfo worked")
    // Set the information in the modal body
    document.getElementById('exampleModal').querySelector('.modal-body').innerHTML = 'Are you sure you want to delete ' + name + '?';

    // Set the link in the modal footer
    var confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    confirmDeleteBtn.href = '{{url_for(url, id=id)}}';
  }

console.log("hi from components.js")