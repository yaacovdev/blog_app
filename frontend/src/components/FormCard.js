const FormCard = {
    template: `
         <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-sm-12 col-md-8 col-lg-6">
                <div class="card shadow-sm p-4">
                    <h2 class="text-center mb-4">{{ title }}</h2>
                    <slot></slot>
                </div>
            </div>
        </div>
    </div>
    `,
    props: ['title'],
    
};

export default FormCard;