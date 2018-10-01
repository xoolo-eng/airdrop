pragma solidity ^0.4.24;

contract StoreVar {
    uint8 public _myVar;
    event MyEvent(uint8 indexed _var);

    function setVar(uint8 _var) public {
        _myVar = _var;
        MyEvent(_var);
    }

    function getVar() public view returns(uint8) {
        return _myVar;
    }
}