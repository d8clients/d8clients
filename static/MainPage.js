function addList() {
    let parent = document.getElementsByTagName("ul")[1];
    let li = document.createElement("li");
    li.className = "list";
    parent.appendChild(li)

    let a = document.createElement('a');
    a.className = "nav-link";
    li.appendChild(a)

    let div = document.createElement('div');
    div.className = "item-4by3 block";
    a.appendChild(div)
}

function myFunctionHide() {
    document.getElementById("myDropdownCategory").classList.toggle("none");
    document.getElementById("myDropdownSpecialist").classList.toggle("none");
  }

function myFunctionCategory() {
    document.getElementById("myDropdownCategory").classList.toggle("show");
  }
  
  function filterFunctionCategory() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInputCategory");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdownCategory");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
      txtValue = a[i].textContent || a[i].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
      } else {
        a[i].style.display = "none";
      }
    }
  }

  function myFunctionSpecialist() {
    document.getElementById("myDropdownSpecialist").classList.toggle("show");
  }
  
  function filterFunctionSpecialist() {
    var input, filter, ul, li, a, i;
    input = document.getElementById("myInputSpecialist");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdownSpecialist");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
      txtValue = a[i].textContent || a[i].innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        a[i].style.display = "";
      } else {
        a[i].style.display = "none";
      }
    }
  }

    