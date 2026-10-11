// Get HTML elements
const expenseForm = document.getElementById("expense-form");
const amountInput = document.getElementById("amount");
const categoryInput = document.getElementById("category");
const descriptionInput = document.getElementById("description");

const expenseList = document.getElementById("expense-list");
const totalExpenses = document.getElementById("total-expenses");
const transactionCount = document.getElementById("transaction-count");

// Load saved expenses from browser storage
let expenses = JSON.parse(localStorage.getItem("expenses")) || [];

// Save expenses
function saveExpenses() {
    localStorage.setItem("expenses", JSON.stringify(expenses));
}

// Display expenses on the page
function displayExpenses() {
    expenseList.innerHTML = "";

    let total = 0;

    if (expenses.length === 0) {
        const message = document.createElement("li");
        message.textContent = "No expenses yet. Add your first one!";
        expenseList.appendChild(message);
    }

    expenses.forEach(function (expense, index) {
        total += expense.amount;

        const item = document.createElement("li");

        const details = document.createElement("div");

        const title = document.createElement("strong");
        title.textContent = expense.description;

        const info = document.createElement("p");
        info.textContent =
            expense.category + " • " + expense.date;

        const price = document.createElement("p");
        price.textContent = "₹" + expense.amount.toFixed(2);

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", function () {
            expenses.splice(index, 1);
            saveExpenses();
            displayExpenses();
        });

        details.appendChild(title);
        details.appendChild(info);

        item.appendChild(details);
        item.appendChild(price);
        item.appendChild(deleteButton);

        expenseList.appendChild(item);
    });

    totalExpenses.textContent = "₹" + total.toFixed(2);
    transactionCount.textContent = expenses.length;
}

// Add a new expense
expenseForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const amount = Number(amountInput.value);
    const category = categoryInput.value;
    const description = descriptionInput.value.trim();

    if (!Number.isFinite(amount) || amount <= 0) {
        alert("Please enter a valid amount.");
        return;
    }

    if (!category || !description) {
        alert("Please complete all fields.");
        return;
    }

    const expense = {
        amount: amount,
        category: category,
        description: description,
        date: new Date().toISOString().split("T")[0]
    };

    expenses.push(expense);

    saveExpenses();
    displayExpenses();

    expenseForm.reset();
});

// Display saved expenses when the page opens
displayExpenses();
