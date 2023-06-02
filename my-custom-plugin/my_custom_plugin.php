<?php
/*
Plugin Name: My Custom Plugin
Description: Adds custom functionality to my WordPress site
*/

// Register custom endpoint for form submission
add_action('rest_api_init', function() {
    register_rest_route('myplugin/v1', '/submit_form', array(
        'methods' => 'POST',
        'callback' => 'submit_form_data',
    ));
});


// Callback function for form submission
function submit_form_data(WP_REST_Request $request) {
    $age = $request->get_param('age');
    $sex = $request->get_param('sex');
    $cp = $request->get_param('cp');
    $trestbps = $request->get_param('trestbps');
    $chol = $request->get_param('chol');
    $fbs = $request->get_param('fbs');
    $restecg = $request->get_param('restecg');
    $thalach = $request->get_param('thalach');
    $exang = $request->get_param('exang');
    $oldpeak = $request->get_param('oldpeak');
    $slope = $request->get_param('slope');
    $ca = $request->get_param('ca');
    $thal = $request->get_param('thal');


 // Send form data to Python backend
    $response = wp_remote_post('http://127.0.0.1:5000/process_form', array(
        'method' => 'POST',
        'body' => array(
            'age' => $age,
            'sex' => $sex,
            'cp' => $cp,
            'trestbps' => $trestbps,
            'chol' => $chol,
            'fbs' => $fbs,
            'restecg' => $restecg,
            'thalach' => $thalach,
            'exang' => $exang,
            'oldpeak' => $oldpeak,
            'slope' => $slope,
            'ca' => $ca,
            'thal' => $thal

        ),
    ));
    
    if (is_wp_error($response)) {
        return new WP_Error('server_error', 'Failed to connect to backend', array('status' => 500));
    }
    
    $response_body = json_decode(wp_remote_retrieve_body($response), true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        return new WP_Error('server_error', 'Failed to parse backend response', array('status' => 500));
    }
    
    $response_data = array('Your Report' => $response_body);
    return new WP_REST_Response($response_data, 200, array('Content-Type' => 'application/json'));


}

add_action('rest_api_init', function() {
    register_rest_route('myplugin/v1', '/process_form_response', array(
        'methods' => 'POST',
        'callback' => 'process_form_response',
    ));
});

function process_form_response(WP_REST_Request $request) {
    $data = $request->get_json_params();
    error_log("Response data: " . print_r($data, true));
    
    // Decode the JSON-encoded result 
    $result_decoded = json_decode($data, true);
    error_log("new: " . print_r($result_decoded, true));

    // Check if the decoding was successful
    if ($result_decoded === null) {
        error_log("Failed to decode result data: " . json_last_error_msg());
        return new WP_REST_Response('Error: Failed to decode result data', 500);
    }

    // Check if the result contains an error message
    if (isset($result_decoded['error'])) {
        return new WP_REST_Response('Error: ' . $result_decoded['error'], 500);
    }


    return new WP_REST_Response($result_decoded, 200);
}
