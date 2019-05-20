  Blockly.Blocks['sen_se'] = {
  init: function() {
    this.jsonInit({
  "type": "sen_se",
  "message0": "se %1 %2 = %3 %4",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "sensores",
      "options": [
        [
          "sensor1",
          "sensor1"
        ],
      ]
    },
    {
      "type": "field_dropdown",
      "name": "condicao",
      "options": [
        [
          ">",
          ">"
        ],
        [
          "<",
          "<"
        ],
        [
          "=",
          "="
        ]
      ]
    },
    {
      "type": "input_value",
      "name": "Se"
    },
    {
      "type": "input_statement",
      "name": "Se_sta",
      "align": "RIGHT"
    }
  ],
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
    });
  }
};


Blockly.Blocks['dispo_out'] = {
  init: function() {
    this.jsonInit({
		"type": "dispo_out",
  "message0": "Dispositivo %1 = %2",
  "args0": [
    {
      "type": "field_dropdown",
      "name": "dispo",
      "options": [
        [
          "dispo1",
          "dispo1"
        ],
        [
          "dispo2",
          "dispo2"
        ],
        [
          "dispo3",
          "dispo3"
        ]
      ]
    },
    {
      "type": "field_number",
      "name": "var",
      "value": 0
    }
  ],
  "previousStatement": null,
  "nextStatement": null,
  "colour": 230,
  "tooltip": "",
  "helpUrl": ""
	});
	}
};

Blockly.Python['dispo_out'] = function(block) {
  var dropdown_dispo = block.getFieldValue('dispo');
  var number_name = block.getFieldValue('NAME');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};

Blockly.Python['sen_se'] = function(block) {
  var dropdown_sensores = block.getFieldValue('sensores');
  var dropdown_condicao = block.getFieldValue('condicao');
  var value_se = Blockly.Python.valueToCode(block, 'Se', Blockly.Python.ORDER_ATOMIC);
  var statements_se_sta = Blockly.Python.statementToCode(block, 'Se_sta');
  // TODO: Assemble Python into code variable.
  var code = '...\n';
  return code;
};