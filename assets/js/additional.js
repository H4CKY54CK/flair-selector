    var character_choice = 0;
    var message = "";

    function majSrc(IDG){
        character_choice = IDG;
		$("#iframe_src").html(`<img src="./images/${IDG}.png" class="thum_character-list" alt="character">`);
	} 

    function sendFlair(){
        if (character_choice === 0) {
            alert('Choose a character before!');
            return;
        }

        message = $("#sendFlair-text").val();

        if (message.length !== 0) {
            if (message.length > 64) {
                alert('64 characters maximum in the Text!');
                return; 
            } else {
                message = `,${message}`;
            }
        } else {
            message = '';
        }
            
        window.open(`https://www.reddit.com/message/compose/?to=MHCP-001&subject=flair&message=${character_choice}${message}`);
    }

    function tutoFlair()
    {
        if (document.getElementById('details_flair-tuto').style.display == 'block'){
            document.getElementById('details_flair-tuto').style.display = 'none';
        } else {
            document.getElementById('details_flair-tuto').style.display = 'block';
        }
    }
