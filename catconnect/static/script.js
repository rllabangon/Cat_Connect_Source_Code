$(document).ready( function () {
    $('#myTable').DataTable();


    const btnDeleteCat = document.querySelectorAll('.btnDeleteCat');
    // console.log(btnDeleteCat[0].dataset.catid);

    if (btnDeleteCat) {
        for (let btn of btnDeleteCat) {

            btn.addEventListener('click', (e) => {
               const catid = btn.dataset.catid;
               const catName = btn.dataset.catname;
               document.querySelector('.cat-name').innerText = catName;
               document.getElementById('catid').value = catid;
            }); 
        }
    }

    

});