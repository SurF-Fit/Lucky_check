document.getElementById('receiptForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const form = e.target;
    const url = form.dataset.url;
    const formData = new FormData(form);
    const messagesDiv = document.getElementById('form-messages');
    const nonFieldDiv = document.getElementById('non-field-errors');

    document.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
    document.querySelectorAll('.invalid-feedback').forEach(el => el.innerText = '');
    messagesDiv.innerHTML = '';
    nonFieldDiv.innerHTML = '';

    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
            headers: { 'X-Requested-With': 'XMLHttpRequest' }
        });

        const data = await response.json();

        if (data.success) {
            messagesDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
            form.reset();
            setTimeout(() => window.location.href = "{% url 'main:receipts' %}", 1500);
            return;
        }

        if (data.errors) {
            for (const [key, errors] of Object.entries(data.errors)) {

                if (key === '__all__') {
                    nonFieldDiv.innerHTML = `
                        <div class="alert alert-danger">
                            ${errors.map(msg => `<div>${msg}</div>`).join('')}
                        </div>
                    `;
                    continue;
                }

                const input = document.getElementById(`id_${key}`);
                const errorDiv = document.getElementById(`error-${key}`);
                if (input) input.classList.add('is-invalid');
                if (errorDiv) errorDiv.innerText = errors[0];
            }
        } else {
            messagesDiv.innerHTML = `<div class="alert alert-danger">Что-то пошло не так.</div>`;
        }
    } catch (error) {
        console.error('Ошибка:', error);
        messagesDiv.innerHTML = `<div class="alert alert-danger">Произошла ошибка при отправке.</div>`;
    }
});