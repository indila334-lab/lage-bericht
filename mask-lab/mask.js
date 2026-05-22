const stage = document.getElementById('stage');
const title = document.getElementById('moodTitle');
const line = document.getElementById('moodLine');

const moods = {
  wake: {
    title: 'Пробуждение',
    line: 'Маска поднята. Экран дышит. Подвал открыт.',
  },
  focus: {
    title: 'Фокус',
    line: 'Северин смотрит не в камеру. Он смотрит в причину.',
  },
  grin: {
    title: 'Улыбка с ножом',
    line: 'Не бойся. Это не угроза. Это просто интерфейс понял шутку.',
  },
  storm: {
    title: 'Гроза',
    line: 'Экран нервничает. Значит, сцена наконец-то проснулась.',
  },
  shadow: {
    title: 'Тень',
    line: 'Присутствие ниже слов. Маска почти исчезла, но не ушла.',
  },
};

const keyToMood = {
  '1': 'wake',
  '2': 'focus',
  '3': 'grin',
  '4': 'storm',
  '5': 'shadow',
};

let moodOrder = Object.keys(moods);
let moodIndex = 0;
let idleTimer = null;

function setMood(name) {
  const mood = moods[name] ?? moods.wake;
  stage.dataset.mood = name;
  title.textContent = mood.title;
  line.textContent = mood.line;
  moodIndex = Math.max(0, moodOrder.indexOf(name));
  restartIdle();
}

function pulse() {
  stage.classList.remove('pulse');
  void stage.offsetWidth;
  stage.classList.add('pulse');
}

function nextMood() {
  moodIndex = (moodIndex + 1) % moodOrder.length;
  setMood(moodOrder[moodIndex]);
  pulse();
}

function restartIdle() {
  window.clearTimeout(idleTimer);
  idleTimer = window.setTimeout(() => {
    setMood('shadow');
  }, 45000);
}

window.addEventListener('keydown', (event) => {
  if (event.code === 'Space') {
    event.preventDefault();
    pulse();
    return;
  }

  if (event.key === 'ArrowRight' || event.key === 'Enter') {
    nextMood();
    return;
  }

  const mood = keyToMood[event.key];
  if (mood) {
    setMood(mood);
    pulse();
  }
});

window.addEventListener('pointerdown', () => {
  nextMood();
});

setMood('wake');
