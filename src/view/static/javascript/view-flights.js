// animating clouds
function animateClouds(){
    let clouds = document.querySelectorAll('.cloud');
    clouds.forEach( (cloud, index) => {
        gsap.from( cloud, {
            y: 400,
            opacity: 0.5,
            duration: 0.5 * index + 1
        });
    });
}

// Functions to help fill table
function getFlagsMapping () {
    let mapping = {};
    const url = 'https://countriesnow.space/api/v0.1/countries/flag/unicode';
    const parameters = {
        method: 'GET'
    };
    fetch(url, parameters)
    .then( data => {
        return data.json()
    })
    .then( response => {
        response.data.forEach((responseData) => {
            mapping[responseData.name] = responseData.unicodeFlag
        });
    })
    .catch( error => {
        console.log(error)
    });
    return mapping;
}

function getCountriesMapping () {
    let mapping = {};
    const url = 'https://countriesnow.space/api/v0.1/countries/population/cities';
    const parameters = {
        method: 'GET'
    };
    fetch(url, parameters)
    .then( data => {
        return data.json()
    })
    .then( response => {
        response.data.forEach((responseData) => {
            mapping[responseData.city] = responseData.country
        });
    })
    .catch( error => {
        console.log(error)
    });
    return mapping;
}

const flagemojiToPNG = (flag) => {
    try{    
        var countryCode = Array.from(flag, (codeUnit) => codeUnit.codePointAt()).map(char => String.fromCharCode(char-127397).toLowerCase()).join('')
        return "<img src='https://flagcdn.com/24x18/" + countryCode + ".png'>"
    }catch(error){
        return "<img src='https://flagcdn.com/24x18/" + countryCode + ".png'>"
    }

}

async function getFlights(cityName) {
    const endPoint = 'http://127.0.0.1:5000/current_flights';
    const data = {
        city: cityName,
    }
    const parameters = {
        method: 'POST',
        body: JSON.stringify(data)
    };

    let flights;
    let responseCode = 0;

    await fetch(endPoint, parameters)
    .then( data => {
        return data.json();
    })
    .then( response => {
        console.log(response)
        flights = response.flights;
        responseCode = response.codePointAt;
    })
    .catch( error => {
        responseCode = -2;
    });

    if (responseCode < 0) {
        console.log('error on request')
    }
    return flights
}

// Constants for filling table
const flagsMapping = getFlagsMapping();
const countriesMapping = getCountriesMapping();

// FLAGS ARE STILL NOT WORKING
// the mapping above has superposition (e.g. london, Canada is a fucking city )
// also nothing with a ~ gets mapped, fucking imperialists

function fillTable(cityName) {
    let rowsContainer = document.querySelector('.content-rows');
    rowsContainer.innerHTML = '';
    getFlights(cityName).then (flightData => {
        flightData.forEach((flight) => {
            // let country = countriesMapping[flight.city]
            // let flag = flagsMapping[country]
            // let flagPNG = flagemojiToPNG(flag)
            rowsContainer.innerHTML += 
            `
                <div class="content-row">
                    <p class="city">${flight.city}</p>
                    <p class="price">${flight.price}</p>
                </div>
            `
        });
    });       
}


function addListeners() {
    let searchButton = document.querySelector('.search-button')
    searchButton.addEventListener('click', () => {
        console.log('searching')
        let cityName = document.querySelector('#leave-from').value;
        if(cityName == ''){window.alert('Please enter a city name.')}
        else{fillTable(cityName);}
    });

    let subscribeButton = document.querySelector('.subscribe-button')
    subscribeButton.addEventListener('click', () => {
        window.location.href = "/";
    })
};

addListeners();
animateClouds();