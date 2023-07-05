#!/bin/bash -e
while getopts ':e:p:t:' OPTION; do
    case $OPTION in
        e)
          # Environment name
          ENVIRONMENT="$OPTARG"
          echo "The name of the environment is $ENVIRONMENT" ;;
        p)
          # Use 1Password to bootstrap secrets or not.  Set to 1 to enable
          USE_ONE_PASSWORD="$OPTARG"
          echo " one password is $USE_ONE_PASSWORD" ;;
        t)
          #1 Password Connect token
          OP_CONNECT_TOKEN="$OPTARG"
          echo " one password is $USE_ONE_PASSWORD" ;;
        *)
          # Printing error message
          echo echo "Usage: $(basename $0) [-e] [-p] [-t]"
          exit 1
          ;;
    esac
done


export OP_CONNECT_HOST=https://roundtable.lsst.codes/1password
export VAULT_DOC_UUID=`yq -r .onepasswordUuid ../environments/values.yaml`
set ${VAULT_ADDR:=https://vault.lsst.codes}
set ${VAULT_TOKEN=`./vault_key.py $ENVIRONMENT write`}


echo "Clear out any existing secrets"
rm -rf secrets

echo "Reading current secrets from vault"
./read_secrets.sh $ENVIRONMENT

if [ "${USE_ONE_PASSWORD}" == 1 ]; then
    echo "Generating missing secrets with values from 1Password"
    ./generate_secrets.py $ENVIRONMENT --op
else
    echo "Open Password disabled.  Generating missing secrets"
    ./generate_secrets.py $ENVIRONMENT 
fi

echo "Writing secrets to vault"
./write_secrets.sh $ENVIRONMENT
