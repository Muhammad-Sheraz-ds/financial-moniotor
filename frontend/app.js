// Get the elements from the DOM
const form = document.getElementById('transaction-form');
const descriptionInput = document.getElementById('description');
const amountInput = document.getElementById('amount');
const categoryInput = document.getElementById('category');
const dateInput = document.getElementById('date');
const analysisResult = document.getElementById('analysis-result');
const getAnalysisButton = document.getElementById('get-analysis');

// Handle form submission to add a transaction
form.addEventListener('submit', async (event) => {
  event.preventDefault(); // Prevent form from reloading the page

  const transactionData = {
    description: descriptionInput.value,
    amount: parseFloat(amountInput.value),
    category: categoryInput.value,
    date: dateInput.value,
  };

  // Send the transaction data to the backend (FastAPI)
  try {
    const response = await fetch('http://127.0.0.1:8000/transactions/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(transactionData),
    });

    const result = await response.json();
    alert('Transaction added successfully');
    form.reset(); // Reset the form fields after submission
  } catch (error) {
    alert('Error adding transaction');
  }
});

// Get financial analysis when the button is clicked
getAnalysisButton.addEventListener('click', async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/analysis/');
    const result = await response.json();
    analysisResult.textContent = result.analysis;
  } catch (error) {
    alert('Error fetching analysis');
  }
});
