package main

import (
	"fmt"
	"os"
	"time"

	"gopkg.in/urfave/cli.v1"
)

func main() {

	app := cli.NewApp()
	app.Name = "alohomora"
	app.Usage = "secret distribution tool"
	app.UsageText = "Alohomora - a secret distribution tool based on aws KMS and dyanmoDB"
	app.Version = "0.0.1"
	app.Authors = []cli.Author{
		cli.Author{
			Name:  "Joy Bhattacherjee",
			Email: "joy.bhattacherjee@razorpay.com",
		},
	}
	app.Compiled = time.Now()
	app.EnableBashCompletion = true

  var flag_region string
  var flag_env string

	app.Flags = []cli.Flag{
		cli.StringFlag{
			Name: "region, R",
      Value: "ap-south-1",
      EnvVar: "AWS_REGION",
      Usage: "`AWS_REGION` for unicreds datastore",
      Destination: &flag_region,
    },
		cli.StringFlag{
      Name: "env, E",
      Value: "prod",
      EnvVar: "APP_ENV,APP_MODE",
      Usage: "Application `env`, used for namespacing",
      Destination: &flag_env,
    },
	}

	app.Commands = []cli.Command{
		{
			Name:      "cast",
			Usage:     "Render a comma separated list of golang template files",
      ArgsUsage: "[APP] [FILES,...]",
      Before: func(c *cli.Context) error {
        fmt.Println("Casting: ", c.Args()[1], "For app: ", c.Args()[0])
        return nil
      },
			Action: func(c *cli.Context) error {
				fmt.Println("Rendered: ", c.Args().First())
				return nil
			},
		},
		{
			Name:    "create",
			Usage:   "Create a credstash database for an application",
      ArgsUsage: "[APP]",
			Action: func(c *cli.Context) error {
				fmt.Println("Created table for app: ", c.Args().First())
				return nil
			},
		},
		{
			Name:    "store",
			Usage:   "Add / Remove a secret for an application's unicreds store",
			Subcommands: []cli.Command{
				{
					Name:  "add",
					Usage: "add a new template",
          ArgsUsage: "[APP] [KEY] [SECRET]",
					Action: func(c *cli.Context) error {
						fmt.Println("Added key: ", c.Args().First(), "for")
						return nil
					},
				},
				{
					Name:  "remove",
					Usage: "remove an existing template",
          ArgsUsage: "[APP] [KEY] [SECRET]",
					Action: func(c *cli.Context) error {
						fmt.Println("removed task template: ", c.Args().First())
						return nil
					},
				},
			},
		},
	}

	app.Run(os.Args)
}
