const backendEndpoint = 'https://g-flights-backend.herokuapp.com';

function sendFlights() {
    const endPoint = backendEndpoint + '/send_flights';
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
    const endPoint = backendEndpoint + '/update_flights';
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
    const endPoint = backendEndpoint + '/users';
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