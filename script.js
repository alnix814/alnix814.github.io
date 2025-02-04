const buttons = document.querySelectorAll('button');
const div_home = document.getElementById('myDiv');
const loading_lo = '<div class="lds-heart"><div></div></div>';
const snowfallContainer = document.getElementById('snowfall');

buttons.forEach(button => {
    button.addEventListener('click', () => {
        div_home.innerHTML = loading_lo;
        setTimeout(() => {
            div_home.innerHTML = '<h1 class="text-2xl font-bold">Я тоже тебя люблю</h1>';
            startSnowfall();
        }, 1000);
    });
});

function createSnowflake() {
    const snowflake = document.createElement('div');
    snowflake.classList.add('snowflake');

    const startX = Math.random() * window.innerWidth;
    snowflake.style.left = `${startX}px`;

    snowflake.style.top = `${-10}px`;

    const fallSpeed = Math.random() * 5 + 2;
    snowflake.style.animationDuration = `${fallSpeed}s`;

    const driftSpeed = Math.random() * 5 + 2;
    snowflake.style.animation = `fall ${fallSpeed}s linear infinite, drift ${driftSpeed}s ease-in-out infinite`;

    snowfallContainer.appendChild(snowflake);

    snowflake.addEventListener('animationiteration', () => {
        snowflake.style.top = `${Math.random() * window.innerHeight}px`;
        snowflake.style.left = `${Math.random() * window.innerWidth}px`;
    });
}

function startSnowfall() {
    const numberOfSnowflakes = 100;
    for (let i = 0; i < numberOfSnowflakes; i++) {
        createSnowflake();
    }
}