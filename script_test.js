const postData = {

    "pname": "Test",
    "pdescription": "Powerful motorized treadmill for home use",
    "pprice": "999.99",
    "pstock": 20
}

fetch('http://127.0.0.1:8000/gym_products/products/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(postData)
})
    .then(response => {
        if(!response.ok){
            throw new Error('Not working')
        }
        return response.json()
    })
    .then(data => {

        console.log(data);
    })
    .catch(error => {
        console.error('Hubo un problema con la solicitud fetch', error)
    })