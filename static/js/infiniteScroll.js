const fetchPage = async (url) => {
    let headers = new Headers()
    headers.append("X-Requested-With", "XMLHttpRequest")
    return fetch(url, { headers })
}

document.addEventListener("DOMContentLoaded", () => {
    let sentinel = document.getElementById("sentinel");
    let scrollElement = document.getElementById("scrollable-element");
    let counter = 2;
    let end = false;

    let observer = new IntersectionObserver(async (entries) => {
        entry = entries[0];
        if (entry.intersectionRatio > 0) {
            let url = document.location.pathname + `?page=${counter}`;
            let req = await fetchPage(url);
            if (req.ok) {
                let body = await req.text();
                // Be careful of XSS if you do this. Make sure
                // you remove all possible sources of XSS.
                scrollElement.innerHTML += body;
                counter++;
            } else {
                // If it returns a 404, stop requesting new items
                end = true;
            }
        }
    })
    observer.observe(sentinel);
})