Blockly.Python['dispo_out'] = function(block) {
  var variable_name = Blockly.Python.variableDB_.getName(block.getFieldValue('dispo'), Blockly.Variables.NAME_TYPE);
  var number_name = block.getFieldValue('var');
  // TODO: Assemble Python into code variable.
  var code = 'save '+variable_name+' '+number_name+'\n';
  return code;
};

Blockly.Python['sen_se'] = function(block) {
  var dropdown_sensores = block.getFieldValue('sensores');
  var dropdown_condicao = block.getFieldValue('condicao');
  var value_se = Blockly.Python.valueToCode(block, 'Se', Blockly.Python.ORDER_ATOMIC);
  var statements_se_sta = Blockly.Python.statementToCode(block, 'Se_sta');
  // TODO: Assemble Python into code variable.
  var code = 'se '+dropdown_sensores+' '+ dropdown_condicao+' '+value_se+'\n'+statements_se_sta+"\n";
  return code;
};