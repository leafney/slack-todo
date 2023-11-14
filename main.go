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
	"github.com/leafney/slack-togo/core"
	"github.com/leafney/slack-togo/global"
	"github.com/leafney/slack-togo/model"
	"github.com/leafney/slack-togo/pkg/parser"
	"github.com/slack-go/slack"
	"log"
)

func main() {

	core.InitCofnig()

	cfg := global.GConfig

	api := slack.New(cfg.BotToken)

	//ConversationHistory(api, cfg)

	ConversationReplies(api, cfg, "1694955326.031139")

	//PostMessage(api, cfg)

}

// 历史消息记录
func ConversationHistory(api *slack.Client, cfg *model.Slack) {
	// 获取历史消息记录
	// - [conversations.history method | Slack](https://api.slack.com/methods/conversations.history)
	result, err := api.GetConversationHistory(&slack.GetConversationHistoryParameters{
		IncludeAllMetadata: true,
		Limit:              1000,
		ChannelID:          cfg.ChannelID,
	})
	if err != nil {
		log.Println(err)
		return
	}

	//data := rose.JsonMarshalStr(result)
	//log.Println(data)
	//rose.FWriteFile("111.json", data, false)
	//for _, msg := range result.Messages {
	//	msg.
	//}

	msgs := parser.ParseConversationHistory(result)
	rose.FWriteFile("222.json", rose.JsonMarshalStr(msgs), false)

}

// 二级内容列表
func ConversationReplies(api *slack.Client, cfg *model.Slack, ts string) {
	//	获取消息项的回复列表
	//- [conversations.replies method | Slack](https://api.slack.com/methods/conversations.replies)
	result, _, _, _ := api.GetConversationReplies(&slack.GetConversationRepliesParameters{
		IncludeAllMetadata: true,
		Timestamp:          ts,
		ChannelID:          cfg.ChannelID,
		Limit:              1000,
	})

	//data := rose.JsonMarshalStr(result)
	//rose.FWriteFile("444.json", data, false)

	msgs := parser.ParseConversationReplies(result, false)
	data := rose.JsonMarshalStr(msgs)
	rose.FWriteFile("555.json", data, false)

}

// 发送消息
func PostMessage(api *slack.Client, cfg *model.Slack) {
	//	发送消息
	//- [chat.postMessage method | Slack](https://api.slack.com/methods/chat.postMessage)
	resCid, resTs, _ := api.PostMessage(
		cfg.ChannelID,
		slack.MsgOptionText("Hello world as User 666", false),
		slack.MsgOptionAsUser(true),
		slack.MsgOptionUser(cfg.UserID),
		slack.MsgOptionTS("1694955326.031139"), // 作为另一条消息的回复内容
	)

	log.Printf("result channelid %s timestamp %s", resCid, resTs)
}
