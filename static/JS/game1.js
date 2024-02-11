// Draggable items and dropzone interaction
interact('#drag1, #drag2, #drag3, #drag4, #drag5, #drag6')
  .draggable({
    inertia: true,
    modifiers: [
      interact.modifiers.restrictRect({
        restriction: 'body',
        endOnly: true
      })
    ],
    autoScroll: true,
    onmove: dragMoveListener
  });

function dragMoveListener(event) {
  var target = event.target,
    x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx,
    y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

  target.style.webkitTransform =
    target.style.transform =
    'translate(' + x + 'px, ' + y + 'px)';

  target.setAttribute('data-x', x);
  target.setAttribute('data-y', y);
}

// Game variables
var score = 0;
var total_items = 12;
var items_played = 0;

// Dropzone logic
function setupDropzone(dropzoneId, correctMaterialType) {
  interact(dropzoneId).dropzone({
    accept: '#drag1, #drag2, #drag3, #drag4, #drag5, #drag6',
    overlap: 0.75,

    ondropactivate: function (event) {
      event.target.classList.add('drop-active');
    },
    ondrop: function (event) {
      var droppedElementId = event.relatedTarget.id;
      var materialType = document.getElementById(droppedElementId).getAttribute('materialtype');

      if (materialType == correctMaterialType) {
        document.getElementById('dropSoundCorrect').play();
        score++;  // Score increments for correct drops
      } else {
        document.getElementById('dropSoundWrong').play();
      }

      document.getElementById(droppedElementId).style.display = 'none';
      items_played++;

      if (items_played == total_items) {
        document.getElementById('user_score').textContent = 'Final Score: ' + score + ' / ' + total_items;
        document.getElementById('drag_item_text').style.display = 'none';
        sendScoreToServer(score);
      } else {
        document.getElementById('user_score').textContent = 'Score: ' + score;
      }
    }
  });
}

// Setting up each dropzone
setupDropzone('#dropzone1', 'glass');
setupDropzone('#dropzone2', 'plastic');
setupDropzone('#dropzone3', 'paper');

// Function to send the score to the server
function sendScoreToServer(score) {
  fetch('/submit_score', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ player_name: playerName, score: score })
  })
    .then(response => response.json())
    .then(data => {
      console.log('Score submission successful:', data);
      getUpdatedScores();
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// Function to get updated scores
function getUpdatedScores() {
  fetch('/get_scores')
    .then(response => response.json())
    .then(data => {
      updateScoreDisplay(data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

// Function to update the score display ##
function updateScoreDisplay(scores) {
  let scoreboard = document.getElementById('scoreboard');
  if (!scoreboard) {
    console.error('Scoreboard element not found');
    return;
  }

  // Create a table element
  let table = document.createElement('table');
  table.classList.add('score-table'); // Add class for styling

  // Create the header row
  let thead = table.createTHead();
  let headerRow = thead.insertRow();
  let headers = ["Player", "Score"];
  for (let headerText of headers) {
    let headerCell = document.createElement("th");
    headerCell.textContent = headerText;
    headerRow.appendChild(headerCell);
  }

  // Create and populate body rows
  let tbody = table.createTBody();
  for (let player in scores) {
    let row = tbody.insertRow();
    let playerCell = row.insertCell();
    playerCell.textContent = player;
    let scoreCell = row.insertCell();
    scoreCell.textContent = scores[player];
  }

  // Clear existing content and add the table
  scoreboard.innerHTML = '';
  scoreboard.appendChild(table);
}

// Original function in case idw table
// function updateScoreDisplay(scores) {
//   let scoreboard = document.getElementById('scoreboard');
//   if (!scoreboard) {
//       console.error('Scoreboard element not found');
//       return;
//   }

//   scoreboard.innerHTML = ''; // Clear current scores

//   for (let player in scores) {
//       let scoreEntry = document.createElement('p');
//       scoreEntry.textContent = `${player}: ${scores[player]}`;
//       scoreboard.appendChild(scoreEntry);
//   }
// }

// Function to store the initial position of the draggable element
function storeInitialPosition(element) {
  const x = (parseFloat(element.getAttribute('data-x')) || 0);
  const y = (parseFloat(element.getAttribute('data-y')) || 0);
  element.setAttribute('data-initial-x', x);
  element.setAttribute('data-initial-y', y);
}

// Function to revert the element to its initial position
function revertToInitialPosition(element) {
  const initialX = parseFloat(element.getAttribute('data-initial-x'));
  const initialY = parseFloat(element.getAttribute('data-initial-y'));
  element.style.transform = `translate(${initialX}px, ${initialY}px)`;
  element.setAttribute('data-x', initialX);
  element.setAttribute('data-y', initialY);
}

// Make the elements draggable
interact('#drag1, #drag2, #drag3, #drag4, #drag5, #drag6')
  .draggable({
    inertia: true,
    modifiers: [
      interact.modifiers.restrictRect({
        restriction: 'parent',
        endOnly: true
      })
    ],
    autoScroll: true,
    onstart: function (event) {
      storeInitialPosition(event.target); // Store the initial position when dragging starts
    },
    onmove: dragMoveListener,
    onend: function (event) {
      // If the element has not been dropped on a dropzone, revert to initial position
      if (!event.interaction.dropTarget) {
        revertToInitialPosition(event.target);
      }
    }
  });

// Existing dragMoveListener function
function dragMoveListener(event) {
  var target = event.target,
    x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx,
    y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

  target.style.webkitTransform =
    target.style.transform =
    'translate(' + x + 'px, ' + y + 'px)';

  target.setAttribute('data-x', x);
  target.setAttribute('data-y', y);
}


document.getElementById('tryAgainButton').addEventListener('click', function() {
  window.location.reload();
});
