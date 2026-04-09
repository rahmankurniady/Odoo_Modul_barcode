/** @odoo-module **/

console.log("✅ Barcode JS Loaded");

document.addEventListener("keydown", function (ev) {

    if (ev.key === "Enter") {

        // ambil SEMUA modal yang tampil
        const modals = document.querySelectorAll('.modal.show, .o_dialog');
        if (!modals.length) return;

        // ambil modal PALING ATAS (terakhir di DOM)
        const topModal = modals[modals.length - 1];

        const button = topModal.querySelector('button[name="action_scan"]');

        if (!button) {
            return;
        }
        else if (button) {
            button.click();
        }
    }
    //console.log(ev.key);

});