document.querySelector('.drop-zone').ondragenter = function() {
    this.style.cursor = 'move';
};
document.querySelector('.drop-zone').ondragleave = function() {
    this.style.cursor = 'pointer';
};
$(document).ready(function() {
    // Click event for a button or icon to toggle the sidebar
    $('#toggle-sidebar').click(function() {
        $('#sidebar-wrapper').toggleClass('active');
    });
});
const toggleFilesButton = document.getElementById('toggleFilesButton');
const fileList = document.getElementById('fileList');

toggleFilesButton.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent the default form submission behavior

    if (fileList.style.display === 'none') {
        fileList.style.display = 'block';
    } else {
        fileList.style.display = 'none';
    }
});

document.addEventListener("DOMContentLoaded", function() {
    const htmlButton = document.getElementById("htmlButton");
    const protoButton = document.getElementById("protoButton");
    const jsonButton = document.getElementById("jsonButton");

    htmlButton.addEventListener("click", function() {
        exportModelCard("html");
    });

    protoButton.addEventListener("click", function() {
        exportModelCard("proto");
    });

    jsonButton.addEventListener("click", function() {
        exportModelCard("json");
    });

    function exportModelCard(format) {
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const url = "{% url 'mc_and_datasheet:createoutput' section.id %}";

        fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": csrfToken,
                },
                body: `format=${format}`,
            })
            .then(response => {
                // Get the content-disposition header to extract the filename
                const contentDisposition = response.headers.get('content-disposition');
                const filename = contentDisposition.split('filename=')[1];

                // Create a blob from the response content
                return response.blob().then(blob => {
                    // Create a blob URL and trigger the download
                    const blobUrl = URL.createObjectURL(blob);
                    const link = document.createElement('a');
                    link.href = blobUrl;
                    link.download = filename;
                    document.body.appendChild(link);
                    link.click();
                    document.body.removeChild(link);
                });
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});
document.getElementById('clearBtn').addEventListener('click', function() {
    var textareas = document.getElementsByClassName('description-answer');
    for (var i = 0; i < textareas.length; i++) {
        textareas[i].value = "";
    }
});

$(document).ready(function() {
    // Get a reference to the Save Changes button
    var saveBtn = document.getElementById("save-btn");

    // Attach a click event listener to the Save Changes button
    saveBtn.addEventListener("click", function() {
        // Get the value of the input field
        var sectionName = document.getElementById("section-name").value;

        // Send the value of the input field to your Django view function
        $.ajax({
            url: "{% url 'mc_and_datasheet:section' section.id %}",
            type: "POST",
            data: {
                'section_name': sectionName,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(response) {
                // Handle the response from your view function
                console.log(response);
            },
            error: function(xhr) {
                // Handle any errors that occur during the request
                console.log(xhr.statusText);
            }
        });
    });
});



src = "https://code.jquery.com/jquery-3.6.0.min.js"
src = "{% static 'mc_and_datasheet/js/jquery-ui.js' %}"

$(function() {
    $('[data-toggle="tooltip"]').tooltip();
});

function saveForm() {
    const newFieldText = document.getElementById('email').value;
    localStorage.setItem('newfieldtext', newFieldText);
}

function clearTextarea() {
    // Get the textarea element by its ID



    var textarea = document.getElementById("description");

    // Clear the textarea by setting its value to an empty string
    textarea.value = "";
}

window.onload = function() {
    const form = document.getElementById('section-form');
    for (let i = 0; i < form.elements.length; i++) {
        const element = form.elements[i];
        if (element.type !== 'button') {
            const value = localStorage.getItem(element.name);
            if (value) {
                element.value = value;
            }
        }
    }
};


// Get the current section ID from the URL
var currentSectionId = '{{ section_id }}';

// Find the link that matches the current section ID and add the 'active' class to it
var links = document.querySelectorAll('.navigation-menu a');
for (var i = 0; i < links.length; i++) {
    var link = links[i];
    if (link.getAttribute('data-section') == currentSectionId) {
        link.classList.add('active');
        break;
    }
}
// Add click event listener to delete buttons
const deleteBtns = document.querySelectorAll('.btn-danger');
deleteBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
        const grandparent = btn.parentNode.parentNode;
        grandparent.parentNode.removeChild(grandparent);
    });
});

// get the date picker input element
const datePicker = document.getElementById('appointment-time');

// get the span element that will display the selected date
const selectedDate = document.getElementById('selected-date');

// add an event listener to the input element that will update the selected date when a new date is selected
datePicker.addEventListener('input', () => {
    selectedDate.textContent = datePicker.value;
});

$(document).ready(function() {
    // Toggle the sidebar on button click for smaller screens
    $('#sidebarToggle').on('click', function() {
        $('#sidebar-wrapper').toggleClass('active');
    });

    // Adjust the sidebar width dynamically based on the window width
    function adjustSidebarWidth() {
        const windowWidth = $(window).width();

        if (windowWidth > 1000) {
            $('#sidebar-wrapper').css('width', '250px');
            $('#main-content').css('margin-left', '250px');
        } else if (windowWidth <= 1000 && windowWidth > 800) {
            $('#sidebar-wrapper').css('width', '70%');
            $('#main-content').css('margin-left', '70%');
        } else if (windowWidth <= 800 && windowWidth > 600) {
            $('#sidebar-wrapper').css('width', '50%');
            $('#main-content').css('margin-left', '50%');
        } else {
            $('#sidebar-wrapper').css('width', '100%');
            $('#main-content').css('margin-left', '0');
        }
    }

    // Call the function initially
    adjustSidebarWidth();

    // Check the initial screen size and adjust the sidebar's class
    function initialSidebarState() {
        const windowWidth = $(window).width();
        if (windowWidth <= 600) {
            $('#sidebar-wrapper').removeClass('active');
        } else {
            $('#sidebar-wrapper').addClass('active');
        }
    }

    // Call the function initially
    initialSidebarState();

    // Call the function on window resize
    $(window).resize(adjustSidebarWidth);
});