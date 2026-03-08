document.addEventListener("DOMContentLoaded", function () {

    function calculateTotal() {
        let subtotal = 0;

        document.querySelectorAll(".item-subtotal").forEach(item => {
            subtotal += parseFloat(item.innerText);
        });

        let tax = subtotal * 0.02;
        let total = subtotal + tax;

        document.getElementById("subtotal").innerText = "₹" + subtotal;
        document.getElementById("tax").innerText = "₹" + tax.toFixed(2);
        document.getElementById("total").innerText = "₹" + total.toFixed(2);
    }

    calculateTotal();
});