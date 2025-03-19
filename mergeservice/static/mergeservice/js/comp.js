let semi_radio_buttons = document.querySelectorAll('.select_section button');
let data_boxs = document.querySelectorAll('section div');
let input_filter = document.getElementById('input_filter');
//let cfpran = 0; //count_of_priority_activation_needed
// semi_radio_buttons.forEach(e => {
//     e.style.color = 'red';
// });
function delete_all_checked_params_in_data(){
    data_boxs.forEach(e => {
        e.classList.remove('checked_block');
    });
}
function delete_all_selected_semi_rad_buts(){
    semi_radio_buttons.forEach(e => {
        e.classList.remove('clicked_but');
    });
}
for(let i = 0; i <= semi_radio_buttons.length -1; i++){
    semi_radio_buttons[i].addEventListener("click", function(e){
        if(i == 0){
            delete_all_checked_params_in_data();
            delete_all_selected_semi_rad_buts();
            data_boxs.forEach(e => {
                e.classList.add('checked_block');
            });
            semi_radio_buttons[0].classList.add('clicked_but');
        }else{
            delete_all_checked_params_in_data();
            delete_all_selected_semi_rad_buts();
            let selected_blocks = document.querySelectorAll(`.${semi_radio_buttons[i].value}`);
            selected_blocks.forEach(e => {
                e.classList.add('checked_block');
            });
            semi_radio_buttons[i].classList.add('clicked_but');
        }
    });
}

function change_elem_list_to_dict(list){
    let dict = {};
    for(let elem = 0; elem <= list.length-1; elem++){
        //console.log(data_boxs[elem]);
        dict[elem] = list[elem].textContent.toLowerCase().split(' ');
        //dict_of_blocks_values.push(data_boxs[elem])
    }
    return dict
}

function the_shortest(a, b){
    if(a <= b){
        return a;
    }else{
        return b;
    }
}

function real_priority_index(index){
    if(index > 0){
        while(index > 1){
            index /= 10;
        }
        return index;
    }else{
        return 1;
    }
}

function segregate_priorities_and_letter_searching(list_1, priority_dict, string){
    string = string.split(' ');
    let temperate_string = "";
    let all_coincidence_dict = {};
    let priority_index_decimal = 0;
    let all_coincidence_list = [];
    let list_for_comparison = [];
    if(list_1.length > 1 || string.length > 1){
    console.log('1', string, list_1);
    for(let q = 0; q < list_1.length - 1; q++){
        for(let i = 0; i < string.length - 1; i++){
                if(list_1.hasOwnProperty(string[i])){

                }
                if(list_1[q].length > string[i].length){
                    if(string[i].length > string[i + 1].length){
                        temperate_string = string[i + 1]
                        string[i+1] = string[i]
                        string[i] = temperate_string
                    }
                }else if(list_1[q].length < string[i].length){
                    if(list_1[q].length > list_1[q].length + 1){
                        temperate_string = list_1[q + 1]
                        list_1[q+1] = list_1[q]
                        list_1[q] = temperate_string
                    }
                }
            }
        }
    }
    console.log('2', string, list_1);
    // TODO: Rebuilt filtering and add index replacing algorythm
    for(let list_elem = 0; list_elem < list_1.length; list_elem++){
        for(let string_elem = 0; string_elem < string.length; string_elem++){
                for(let string_length_and_list = 0; string_length_and_list < the_shortest(list_1[list_elem].length, string[string_elem].length); string_length_and_list++){
                    if(list_1[list_elem][string_length_and_list] === string[string_elem][string_length_and_list]){
                        all_coincidence_list.push(string[string_elem][string_length_and_list]);
                        console.log('A', list_1[list_elem], string[string_elem]);
                    }else{
                        priority_index_decimal += 1;
                        console.log(list_1[list_elem], string[string_elem]);
                    }
                }
        }
        console.log(all_coincidence_list, real_priority_index(priority_index_decimal));
        all_coincidence_list = [];
        priority_index_decimal = 0;
    }
}

function custom_search(converted_str, priority_dict_elems){
    let standart_tags = ['grants', 'requests', 'users', 'confirm'];
    let temp_dict = {};
    for(let i = 0; i < standart_tags.length; i++){
        //console.log(converted_str.search(standart_tags[i]));
        if(converted_str.search(standart_tags[i]) > -1){
            let temperate_data_box = document.getElementsByClassName(`checked_block ${standart_tags[i]}`);
            //console.log(standart_tags[i]);
                temp_dict = change_elem_list_to_dict(temperate_data_box);
                console.log(temp_dict);
        }
        //console.log(data_boxs[i].classList.contains(standart_tags[i]));
    }
    if(Object.keys(temp_dict).length < 1){
        temp_dict = change_elem_list_to_dict(data_boxs);
    }
    for(let final_exit_dict_value = 0; final_exit_dict_value < Object.keys(temp_dict).length; final_exit_dict_value++){
        console.log(temp_dict[final_exit_dict_value], priority_dict_elems, converted_str);
        segregate_priorities_and_letter_searching(temp_dict[final_exit_dict_value], priority_dict_elems, converted_str);
    }
}

function filter_request(){
    if(input_filter.value.length > 0){
        let dict_of_blocks_values = {};
        let converted_string = input_filter.value.toLowerCase().split(' ');
        let list_of_finded_elems = [];
        let priority_elem_exit = {};
        dict_of_blocks_values = change_elem_list_to_dict(data_boxs);
            converted_string.forEach(temp_elem => {
                for(let temp_elem_value = 0; temp_elem_value <= Object.keys(dict_of_blocks_values).length -1; temp_elem_value++){
                    if(dict_of_blocks_values[temp_elem_value].indexOf(temp_elem) > -1){
                        if(!(list_of_finded_elems.includes(temp_elem_value))){
                            list_of_finded_elems.push(temp_elem_value);
                        }
                        console.log(`Common elem --> ${list_of_finded_elems}`);
                    }
                }
            });
            if(list_of_finded_elems.length > 0){
                priority_elem_exit[1] = list_of_finded_elems;
            }
            //console.log(dict_of_blocks_values);
            console.log(priority_elem_exit);
            //console.log('Start custom filtering...');
            custom_search(input_filter.value.toLowerCase(), priority_elem_exit);


    }else{
        alert('You need to provide something in order to filter');
    }

}