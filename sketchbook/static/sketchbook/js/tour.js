// intro.js tour for screens up to 1199px wide
const tourMobile = {
    steps: [{
            element: document.querySelector('#tour-start'),
            title: 'Welcome',
            intro: "<p>Welcome to the Doodle This tour.</p><p>Use the buttons below or the arrow keys on your keyboard (if you have one) to take the tour and find out how everything works.</p><p class='mb-0'>You can leave the tour by clicking the X in the top right corner or pressing the Esc key.</p>",
        },
        {
            element: document.querySelector('#scaler-holder'),
            intro: 'This is your sketchbook, where you can doodle whatever you like. Give it a try!'
        },
        {
            element: document.querySelector('#preset-colour-holder'),
            intro: "Drawing with just one colour would get dull. Click on any of these buttons to pick a new colour."
        },
        {
            element: document.querySelector('#cursor-stroke-width'),
            intro: "Notice how this circle changed colour when you clicked the colour buttons? This shows you what colour you'll be drawing with. And you can change the size with the slider. Give it a go!"
        },
        {
            element: document.querySelector('#coloris-tour'),
            intro: `Want <em>even more</em> colours to choose from? Click this box to mix up your own! Give it a try after the tour.`,
            disableInteraction: true
        },
        {
            element: document.querySelector('#tool-holder'),
            intro: "Here's where you'll find the tools of the trade. Four little buttons that will help you make magic!"
        },
        {
            element: document.querySelector('#pencil-tool'),
            intro: "Your pencil is your best friend. You can use it to draw anything you can imagine."
        },
        {
            element: document.querySelector('#fill-tool'),
            intro: "When you need to turn a lot of one colour into another colour, the fill tool is here to help."
        },
        {
            element: document.querySelector('#erase-tool'),
            intro: "The eraser tool has the power to magically change coloured-in space into empty space."
        },
        {
            element: document.querySelector('#picker-tool'),
            intro: "This is the colour picker tool. You can point it at any colour on your canvas and click to grab that colour."
        },
        {
            element: document.querySelector('#undo-bottom'),
            intro: "We believe in happy little accidents here, but just in case you've done something you <em>really</em> didn't want to do, you can undo your last action with this button."
        },
        {
            element: document.querySelector('#clear-bottom'),
            intro: "Or if it's all gone wrong and you just want to start again, you can clear your canvas by clicking here.",
            disableInteraction: true
        },
        {
            element: document.querySelector('#drawing-prompt'),
            intro: 'If you want a drawing prompt to get the creative juices flowing, you can find one right here.'
        },
        {
            element: document.querySelector('#get-prompt-button'),
            intro: "Didn't like your drawing prompt? No problem. Click here to get a new one!"
        },
        {
            element: document.querySelector('#save-load-bottom'),
            intro: "If you have an account, you can save your favourite doodles here and then load them back whenever you like. If you don't have an account, why not <a href='/account/signup/' target='_blank'>sign up</a>? It's free!",
            disableInteraction: true
        },
        {
            element: document.querySelector('#options-bottom'),
            intro: "Finally, you can tweak your sketchbook's options here. After the tour, open up the menu and click the <span class='tour-icon'>?</span> icons to find out what the different settings do.",
            disableInteraction: true
        },
        {
            element: document.querySelector('#help-button'),
            intro: "And that's it! If you ever want a reminder of how everything works, you can click the help button to take the tour again. Now go draw something awesome!",
        },
    ],
    tooltipClass: 'customIntroJs',
    exitOnOverlayClick: false,
    overlayOpacity: 0.7
};

// intro.js tour for screens 1200px wide and above 
const tourDesktop = {
        steps: [{
                element: document.querySelector('#tour-start'),
                title: 'Welcome',
                intro: "<p>Welcome to the Doodle This tour.</p><p>Use the buttons below or the arrow keys on your keyboard (if you have one) to take the tour and find out how everything works.</p><p class='mb-0'>You can leave the tour by clicking the X in the top right corner or pressing the Esc key.</p>",
            },
            {
                element: document.querySelector('#scaler-holder'),
                intro: 'This is your sketchbook, where you can doodle whatever you like. Give it a try!'
            },
            {
                element: document.querySelector('#preset-colour-holder'),
                position: "left",
                intro: "Drawing with just one colour would get dull. Click on any of these buttons to pick a new colour."
            },
            {
                element: document.querySelector('#cursor-stroke-width'),
                position: "left",
                intro: "Notice how this circle changed colour when you clicked the colour buttons? This shows you what colour you'll be drawing with. And you can change the size with the slider. Give it a go!"
            },
            {
                element: document.querySelector('#coloris-tour'),
                position: "left",
                intro: `Want <em>even more</em> colours to choose from? Click this box to mix up your own! Give it a try after the tour.`,
                disableInteraction: true
            },
            {
                element: document.querySelector('#tool-holder'),
                position: "left",
                intro: "Here's where you'll find the tools of the trade. Four little buttons that will help you make magic!"
            },
            {
                element: document.querySelector('#pencil-tool'),
                position: "left",
                intro: "Your pencil is your best friend. You can use it to draw anything you can imagine."
            },
            {
                element: document.querySelector('#fill-tool'),
                position: "left",
                intro: "When you need to turn a lot of one colour into another colour, the fill tool is here to help."
            },
            {
                element: document.querySelector('#erase-tool'),
                position: "left",
                intro: "The eraser tool has the power to magically change coloured-in space into empty space."
            },
            {
                element: document.querySelector('#picker-tool'),
                position: "left",
                intro: "This is the colour picker tool. You can point it at any colour on your canvas and click to grab that colour."
            },
            {
                element: document.querySelector('#undo-side'),
                position: "right",
                intro: "We believe in happy little accidents here, but just in case you've done something you <em>really</em> didn't want to do, you can undo your last action with this button."
            },
            {
                element: document.querySelector('#clear-side'),
                position: "right",
                intro: "Or if it's all gone wrong and you just want to start again, you can clear your canvas by clicking here.",
                disableInteraction: true
            },
            {
                element: document.querySelector('#drawing-prompt'),
                position: "right",
                intro: 'If you want a drawing prompt to get the creative juices flowing, you can find one right here.'
            },
            {
                element: document.querySelector('#get-prompt-button'),
                position: "right",
                intro: "Didn't like your drawing prompt? No problem. Click here to get a new one!"
            },
            {
                element: document.querySelector('#save-load-side'),
                position: "right",
                intro: "If you have an account, you can save your favourite doodles here and then load them back whenever you like. If you don't have an account, why not <a href='/account/signup/' target='_blank'>sign up</a>? It's free!",
                disableInteraction: true
            },
            {
                element: document.querySelector('#options-side'),
                position: "right",
                intro: "Finally, you can tweak your sketchbook's options here. After the tour, open up the menu and click the <span class='tour-icon'>?</span> icons to find out what the different settings do.",
                disableInteraction: true
            },
            {
                element: document.querySelector('#help-button'),
                position: "right",
                intro: "And that's it! If you ever want a reminder of how everything works, you can click the help button to take the tour again. Now go draw something awesome!",
            },
        ],
        tooltipClass: 'customIntroJs',
        exitOnOverlayClick: false,
        overlayOpacity: 0.7
    };