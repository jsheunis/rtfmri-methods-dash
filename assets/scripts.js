$(document).ready(function($) {
    $("#container").on('click-row.bs.table', function (e, row, $element) {
        window.location = $element.data('href');
    });
});



// html.Table([
//                 html.Tbody([
//                     html.Tr([
//                         html.Td(['Kaas']),
//                     ]),
//                     html.Tr([
//                         html.Td(['Koek']),
//                     ]),
//                     html.Tr([
//                         html.Td(['Klap']),
//                     ],
//                         className='table-row',
//                         **{
//                             'data-href': 'https://jsheunis.github.io',
//                         }
//                     )
//                 ]),],
//                 style={
//                     'marginBottom': 25,
//                     'marginTop': 25,
//                     'marginLeft': '5%',
//                     'maxWidth': '90%',
//                 },
//             ),