function my_scope() {
    const forms = document.querySelectorAll('.form-delete')

    for (const form of forms){
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                const confirmed = confirm('Are you sure?');
    
                if (confirmed) {
                    form.submit();
                }
            });
        }
    }
}

my_scope();