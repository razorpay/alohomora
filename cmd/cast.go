package cmd

import (
	//"fmt"
	"os"
	//"time"
	"strings"

	"github.com/Versent/unicreds"
)

func createFileSlice(files string) [] string {
	cleaned := strings.Replace(files, ",", " ", -1)
	fileSlice := strings.Fields(cleaned)
	return fileSlice
}

func getAppSecrets(region string, env string, app string) []*unicreds.DecryptedCredential{
	tableNameString := "credstash-"+env+"-"+app
	var tableName *string = &tableNameString
	allVersions := false
	encContext := unicreds.NewEncryptionContextValue()
	secrets, err := unicreds.GetAllSecrets(tableName, allVersions, encContext)
	if err != nil {
		panic(err)
	}
	return secrets
}

func checkFileForSecrets(file string ) bool {
	// if file has at least one lookup
	return true
	// else return false
}

func castTemplate(secrets []*unicreds.DecryptedCredential, file string ) string {
	var renderedFile string;
	for _, secret := range secrets {
		os.Setenv(secret.Name, secret.Secret)
		// logic for key-lookup in go template
		// substituting with value
	}
	return renderedFile
}

func castFile(region string, env string, app string, file string){
	if checkFileForSecrets(file) {
		castTemplate(getAppSecrets(region, env, app), file)
	}
}

func Cast(region string, env string, app string, files string){
  fileSlice := createFileSlice(files)

	for _, file := range fileSlice{
		castFile(region, env, app, file)
	}
}
