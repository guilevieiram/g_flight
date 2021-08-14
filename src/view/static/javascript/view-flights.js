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

function animatePage( ) {
    let panel = document.querySelector('.flights-panel')

    gsap.to(panel , {
        opacity: 1, 
        duration: 1.5, 
        y: 0
    })
}

function loaderOn() {
    let loader = document.querySelector('.loader')
    gsap.set(loader, {
        display: 'block'
    })
}

function loaderOff() {
    let loader = document.querySelector('.loader')
    gsap.set(loader, {
        display: 'none'
    })
}
// Functions to help fill table
let countryFlagsMapping = {};
function getFlagsMapping () {
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
            let countryName = responseData.name.toLowerCase();
            // handling country names that differ;
            if(countryName === 'united kingdom'){countryName = 'united kingdom of great britain and northern ireland'}
            countryFlagsMapping[countryName] = responseData.unicodeFlag
        });
    })
    .catch( error => {
        console.log(error)
    });
}
// getFlagsMapping();


let cityFlagMapping = [];
function getCountriesMapping () {
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
            let flag = countryFlagsMapping[responseData.country.toLowerCase()]
            let currentPopulation = parseFloat(responseData.populationCounts[0].value);
            let existingCity = (cityFlagMapping.find( ({city}) => city.toLowerCase()===responseData.city.toLowerCase()));
            let existingPopulation = (typeof existingCity != "undefined") ? parseFloat(existingCity.population) : 0;

            if(existingPopulation < currentPopulation){
                if(existingPopulation !== 0){
                    cityFlagMapping = cityFlagMapping.filter(({city}) => {
                        return city.toLowerCase() !== existingCity.city.toLowerCase()
                    })
                }
                cityFlagMapping.push({
                    city: responseData.city,
                    flag: (typeof flag != "undefined") ? flag : 'no flag',
                    population: currentPopulation
                });
            }
        });
    })
    .catch( error => {
        console.log(error)
    });
}
// getCountriesMapping();

const flagemojiToPNG = (flag) => {
    try{    
        var countryCode = Array.from(flag, (codeUnit) => codeUnit.codePointAt()).map(char => String.fromCharCode(char-127397).toLowerCase()).join('')
        return "<img src='https://flagcdn.com/24x18/" + countryCode + ".png'>"
    }catch(error){
        return ""
    }

}

function getFlag(city) {
    let cityUnicode = cityFlagMapping.find(element => {
        return element.city.toLowerCase() === city.toLowerCase();
    })
    let flagUnicode = (typeof(cityUnicode) !== "undefined") ? cityUnicode.flag : undefined    
    return flagemojiToPNG(flagUnicode)
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
        flights = response.flights;
        responseCode = response.code;
    })
    .catch( error => {
        responseCode = -2;
    });

    if (responseCode === -1) {
        window.alert("Couldn't find that location.\nTry another one!");
        loaderOff();
    }
    else if (responseCode === -2) {
        window.alert("Looks like our servers are down...\nTry again later!")
        loaderOff();
    }
    else {return flights}
}




// FLAGS ARE STILL NOT WORKING
// the mapping above has superposition (e.g. london, Canada is a fucking city )
// also nothing with a ~ gets mapped, fucking imperialists

function fillTable(cityName) {
    let rowsContainer = document.querySelector('.content-rows');
    rowsContainer.innerHTML = '';
    getFlights(cityName).then(flightData => {
        if (typeof(flightData) === "undefined"){return}
        flightData.forEach((flight) => {
            rowsContainer.innerHTML += 
            `
                <div class="content-row">
                    <p class="city">${flight.city}</p>
                    <p class="price">${flight.price}</p>
                </div>
            `
        });
        loaderOff();
    });       
}


function addListeners() {
    let searchButton = document.querySelector('.search-button')
    searchButton.addEventListener('click', () => {
        console.log('searching')
        let cityName = document.querySelector('#leave-from').value;
        if(cityName == ''){window.alert('Please enter a city name.')}
        else{
            loaderOn();
            fillTable(cityName);
        }
    });

    let subscribeButton = document.querySelector('.subscribe-button')
    subscribeButton.addEventListener('click', () => {
        window.location.href = "/";
    })
};

addListeners();
animateClouds();
animatePage();