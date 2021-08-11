function sendFlights() {
    const endPoint = 'http://127.0.0.1:5000/send_flights';
    const parameters = {
        method: 'GET'
    };
    fetch(endPoint, parameters)
    .then( data => {
        return data.json()
    })
    .then( response => {
        console.log(response)
    })
    .catch( error => {
        console.log(error)
    });
}

function updateFlights() {
    const endPoint = 'http://127.0.0.1:5000/update_flights';
    const parameters = {
        method: 'GET'
    };
    fetch(endPoint, parameters)
    .then( data => {
        return data.json()
    })
    .then( response => {
        console.log(response)
    })
    .catch( error => {
        console.log(error)
    });
}

async function addUser(name, lastName, email, city) {
    const endPoint = 'http://127.0.0.1:5000/users';
    const data = {
        first_name: name,
        last_name: lastName,
        phone: '0',
        e_mail: email,
        city: city
    }
    const parameters = {
        method: 'POST',
        body: JSON.stringify(data)
    };

    let responseCode = 0;

    await fetch(endPoint, parameters)
    .then( data => {
        return data.json();
    })
    .then( response => {
        responseCode = response.code;
    })
    .catch( error => {
        responseCode = -2;
    });

    return responseCode;
    
}