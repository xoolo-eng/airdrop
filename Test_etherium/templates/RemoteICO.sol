pragma solidity ^0.4.24;
contract ERC20 {
    function transfer(address to, uint value) public;  
}

contract {{ name }} {
    address _contract = {{ contract.contract }};
    address _owner = {{ contract.address }};
    uint _count_tokens = {{ contract.amount }};
    ERC20 _remote_contract;

    function {{ name }}() {
        _remote_contract = ERC20(_contract);
    }

    function transferFor(address[] _to) public {
        if (msg.sender == _owner) {
            for(uint i=0; i<_to.length; ++i) {
                _remote_contract.transfer(_to[i], _count_tokens);
            }
        }
    }
}