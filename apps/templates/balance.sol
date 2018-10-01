pragma solidity ^0.4.24;
contract API {
    function transfer(address to, uint value) public;  
}

contract {{ name.class }} {
    address _contract = {{ contract.address }};
    address _owner = {{ contract.owner }};
    uint _count_tokens = {{ contract.count }};
    API _remote_contract;

    function {{ name.class }}() {
        _remote_contract = API(_contract);
    }

    function transferFor(address[] _to) public {
        if (msg.sender == _owner) {
            for(uint i=0; i<_to.length; ++i) {
                _remote_contract.transfer(_to[i], _count_tokens);
            }
        }
    }
}