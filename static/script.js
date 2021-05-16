function editLoan(loanID) {
  document.getElementById("editLoanModalLabel").innerHTML = "Edit Loan for " + document.getElementById("loan-" + loanID).innerHTML;
  document.getElementById("editLoanID").value = loanID;
}