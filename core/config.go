/**
 * @Author:      leafney
 * @GitHub:      https://github.com/leafney
 * @Project:     slack-togo
 * @Date:        2023-09-23 17:45
 * @Description:
 */

package core

import (
	"github.com/knadh/koanf/parsers/yaml"
	"github.com/knadh/koanf/providers/file"
	"github.com/knadh/koanf/v2"
	"github.com/leafney/slack-togo/global"
	"log"
	"os"
)

var k = koanf.New(".")

func InitCofnig() {
	// 指定多个配置文件路径
	paths := []string{"config/config.yaml", "config.yaml"}

	for _, path := range paths {
		if err := k.Load(file.Provider(path), yaml.Parser()); err == nil {
			log.Printf("[Koanf] Load config file %v", path)
			break
		} else {
			log.Printf("[Koanf] Load config file %v err: %v", path, err)
		}
	}

	if len(k.Keys()) == 0 {
		log.Printf("[Koanf] Config file not exist")
		os.Exit(1)
	}

	if err := k.Unmarshal("", &global.GConfig); err != nil {
		log.Printf("[Koanf] Unmarshal config err %v", err)
		os.Exit(1)
	}

	log.Println("[Koanf] Load config success")
}
