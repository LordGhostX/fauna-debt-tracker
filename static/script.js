function editLoan(loanID) {
  document.getElementById("editLoanModalLabel").innerHTML = "Edit Loan for " + document.getElementById(loanID).innerHTML;
  document.getElementById("editLoanID").value = loanID;
}