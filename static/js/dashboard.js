// for dashboard bottom icon 
const add_event_and_participant_parent=document.getElementById('add_event_and_participant_parent');
add_event_and_participant_parent.addEventListener('click',(e)=>{
    const child=document.getElementById('add_event_and_participant_child')
    const svg_plus_and_cross_button=document.getElementById('svg-plus-and-cross-button')
    if (add_event_and_participant_parent.classList.contains('bg-green-500')) {
        add_event_and_participant_parent.classList.remove('bg-green-500','hover:bg-green-400');
        add_event_and_participant_parent.classList.add('bg-gray-700','hover:bg-gray-600');
        child.classList.remove('scale-0');
        child.classList.add('scale-100');
        svg_plus_and_cross_button.classList.remove('rotate-0');
        svg_plus_and_cross_button.classList.add('rotate-45');
        
    }
    else{
      add_event_and_participant_parent.classList.remove('bg-gray-700','hover:bg-gray-600');
        add_event_and_participant_parent.classList.add('bg-green-500','hover:bg-green-400');
        child.classList.remove('scale-100');
        child.classList.add('scale-0');
        svg_plus_and_cross_button.classList.remove('rotate-45');
        svg_plus_and_cross_button.classList.add('rotate-0');
        
    }
    child.addEventListener('click', (e) => {
        e.stopPropagation();
    });

    });