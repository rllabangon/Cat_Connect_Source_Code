$(document).ready( function () {
    $('#myTable').DataTable();

    // Get all the possible buttons for the delete cat button
    const btnDeleteCat = document.querySelectorAll('.btnDeleteCat');

    if (btnDeleteCat) {
        // Setting a click listener for all delete cat button
        for (let btn of btnDeleteCat) {

            btn.addEventListener('click', (e) => {
               const catid = btn.dataset.catid; // get the cat_id
               const catName = btn.dataset.catname; // get the cat's name
               document.querySelector('.cat-name').innerText = catName; // put the cat's name into delete cat's form
               document.getElementById('catid').value = catid; // put the cat's id into delete cat's form
            }); 
        }
    }

    

});