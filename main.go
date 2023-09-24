/**
 * @Author:      leafney
 * @GitHub:      https://github.com/leafney
 * @Project:     slack-togo
 * @Date:        2023-09-16 23:25
 * @Description:
 */

package main

import (
	"github.com/leafney/rose"
	"github.com/leafney/slack-togo/config"
	"github.com/leafney/slack-togo/global"
	"github.com/leafney/slack-togo/model"
	"github.com/slack-go/slack"
	"log"
)

func main() {

	config.InitCofnig()

	cfg := global.GConfig

	api := slack.New(cfg.BotToken)

	ConversationHistory(api, cfg)

	//PostMessage(api)

}

// 历史消息记录
func ConversationHistory(api *slack.Client, cfg *model.Slack) {
	// 获取历史消息记录
	result, err := api.GetConversationHistory(&slack.GetConversationHistoryParameters{
		IncludeAllMetadata: true,
		Limit:              1000,
		ChannelID:          cfg.ChannelID,
	})
	if err != nil {
		log.Println(err)
		return
	}

	data := rose.JsonMarshalStr(result)
	//log.Println(data)
	rose.FWriteFile("111.json", data, false)
	//for _, msg := range result.Messages {
	//	msg.
	//}

}

// 二级内容列表
func ConversationReplies(api *slack.Client, cfg *model.Slack) {
	//	获取消息项的回复列表
	//- [conversations.replies method | Slack](https://api.slack.com/methods/conversations.replies)
	result, _, _, _ := api.GetConversationReplies(&slack.GetConversationRepliesParameters{
		IncludeAllMetadata: true,
		Timestamp:          "1687698556.243869",
		ChannelID:          cfg.ChannelID,
	})

	data := rose.JsonMarshalStr(result)
	rose.FWriteFile("456.json", data, false)
}

// 发送消息
func PostMessage(api *slack.Client, cfg *model.Slack) {
	//	发送消息
	resCid, resTs, _ := api.PostMessage(
		cfg.ChannelID,
		slack.MsgOptionText("Hello world as User 444", false),
		//slack.MsgOptionAsUser(true),
		//slack.MsgOptionUser("U0563221SBY"),
	)

	log.Printf("result channelid %s timestamp %s", resCid, resTs)
}
