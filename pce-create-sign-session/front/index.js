function formatDate(date) {
    const month = date.getMonth() + 1;
    return date.getFullYear() + "-" + (month < 9 ? "0" + month : month) + "-" + (date.getDate() < 9 ? "0" + date.getDate() : date.getDate());
}

function getDates(strdate) {
    let dates = []
    const date = new Date(strdate);
    if (date.getDay() != 1) {
        while (date.getDay() != 1) {
            date.setDate(date.getDate() + 1);
        }
    }
    document.getElementById('monday').innerHTML = formatDate(date);
    dates.push(formatDate(date));
    date.setDate(date.getDate() + 1)
    document.getElementById('thuesday').innerHTML = formatDate(date);
    dates.push(formatDate(date));
    date.setDate(date.getDate() + 1)
    document.getElementById('wednesday').innerHTML = formatDate(date);
    dates.push(formatDate(date));
    date.setDate(date.getDate() + 1)
    document.getElementById('thursday').innerHTML = formatDate(date);
    dates.push(formatDate(date));
    date.setDate(date.getDate() + 1)
    document.getElementById('friday').innerHTML = formatDate(date);
    dates.push(formatDate(date));
    return dates;
}

function alterIntra() {
    const dates = getDates(Date.now());
    fetch('http://localhost:8000/create_session', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            [{
                'date': dates[0],
                'msc1': document.getElementById('monday-check').children[0].checked,
                'msc2': document.getElementById('monday-check').children[1].checked,
                'wac1': document.getElementById('monday-check').children[2].checked,
                'wac2': document.getElementById('monday-check').children[3].checked,
                'premsc': document.getElementById('monday-check').children[4].checked,
                'codac': document.getElementById('monday-check').children[5].checked
            },
            {
                'date': dates[1],
                'msc1': document.getElementById('thuesday-check').children[0].checked,
                'msc2': document.getElementById('thuesday-check').children[1].checked,
                'wac1': document.getElementById('thuesday-check').children[2].checked,
                'wac2': document.getElementById('thuesday-check').children[3].checked,
                'premsc': document.getElementById('thuesday-check').children[4].checked,
                'codac': document.getElementById('thuesday-check').children[5].checked
            }, {
                'date': dates[2],
                'msc1': document.getElementById('wednesday-check').children[0].checked,
                'msc2': document.getElementById('wednesday-check').children[1].checked,
                'wac1': document.getElementById('wednesday-check').children[2].checked,
                'wac2': document.getElementById('wednesday-check').children[3].checked,
                'premsc': document.getElementById('wednesday-check').children[4].checked,
                'codac': document.getElementById('wednesday-check').children[5].checked
            }, {
                'date': dates[3],
                'msc1': document.getElementById('thursday-check').children[0].checked,
                'msc2': document.getElementById('thursday-check').children[1].checked,
                'wac1': document.getElementById('thursday-check').children[2].checked,
                'wac2': document.getElementById('thursday-check').children[3].checked,
                'premsc': document.getElementById('thursday-check').children[4].checked,
                'codac': document.getElementById('thursday-check').children[5].checked
            }, {
                'date': dates[4],
                'msc1': document.getElementById('friday-check').children[0].checked,
                'msc2': document.getElementById('friday-check').children[1].checked,
                'wac1': document.getElementById('friday-check').children[2].checked,
                'wac2': document.getElementById('friday-check').children[3].checked,
                'premsc': document.getElementById('friday-check').children[4].checked,
                'codac': document.getElementById('friday-check').children[5].checked
            }])
    }).then((response) => {
        return response.json();
    }).catch((err) => {
        throw err;
    });
}