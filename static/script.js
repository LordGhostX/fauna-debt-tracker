function updateLoan(loanID) {
  document.getElementById("updateLoanModalLabel").innerHTML = "Update Loan for " + document.getElementById("loan-" + loanID).innerHTML;
  document.getElementById("updateLoanID").value = loanID;
}